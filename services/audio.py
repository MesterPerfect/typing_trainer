import sys
import os
import platform
import logging
import ctypes
from pathlib import Path
from typing import Optional, Dict
from core.constants import BASE_DIR

logger = logging.getLogger(__name__)

# BASS Constants
BASS_UNICODE = 0x80000000
BASS_SAMPLE_OVER_POS = 0x20000  # Override oldest instance if maximum simultaneous playbacks reached
BASS_ATTRIB_VOL = 2            # Volume attribute (0.0 to 1.0)


class AudioService:
    """
    Ultra-low latency audio service powered by the BASS audio library via ctypes.
    Cross-platform support for Windows, Linux, and macOS with zero external pip dependencies.
    """

    def __init__(self, settings):
        self.settings = settings
        self.bass = None
        self.available = False
        self.samples: Dict[str, int] = {}

        self._init_bass()
        if self.available:
            self._load_all_sounds()

    def _find_bass_library(self) -> Optional[Path]:
        system = platform.system()
        is_64bit = sys.maxsize > 2**32
        machine = platform.machine().lower()

        if system == "Windows":
            arch_dir = "x64" if is_64bit else "x86"
            candidates = [
                BASE_DIR / "assets" / "bass" / "windows" / arch_dir / "bass.dll",
                BASE_DIR / "bass.dll",
                BASE_DIR / "lib" / "bass.dll",
            ]
        elif system == "Darwin":
            candidates = [
                BASE_DIR / "assets" / "bass" / "macos" / "libbass.dylib",
                BASE_DIR / "libbass.dylib",
                BASE_DIR / "lib" / "libbass.dylib",
            ]
        else:  # Linux
            arch_dir = "aarch64" if ("arm" in machine or "aarch64" in machine) else "x86_64"
            candidates = [
                BASE_DIR / "assets" / "bass" / "linux" / arch_dir / "libbass.so",
                BASE_DIR / "libbass.so",
                BASE_DIR / "lib" / "libbass.so",
            ]

        for p in candidates:
            if p.exists():
                return p
        return None

    def _init_bass(self):
        lib_path = self._find_bass_library()
        if not lib_path:
            logger.warning("BASS audio library binary not found. Audio effects will be disabled.")
            return

        try:
            self.bass = ctypes.CDLL(str(lib_path.resolve()))

            # BASS_Init(int device, DWORD freq, DWORD flags, void *win, void *clsid)
            self.bass.BASS_Init.argtypes = [
                ctypes.c_int,
                ctypes.c_ulong,
                ctypes.c_ulong,
                ctypes.c_void_p,
                ctypes.c_void_p
            ]
            self.bass.BASS_Init.restype = ctypes.c_bool

            # BASS_SampleLoad(BOOL mem, void *file, QWORD offset, DWORD length, DWORD max, DWORD flags)
            self.bass.BASS_SampleLoad.argtypes = [
                ctypes.c_bool,
                ctypes.c_void_p,
                ctypes.c_uint64,
                ctypes.c_ulong,
                ctypes.c_ulong,
                ctypes.c_ulong
            ]
            self.bass.BASS_SampleLoad.restype = ctypes.c_ulong

            # BASS_SampleGetChannel(HSAMPLE handle, BOOL onlynew)
            self.bass.BASS_SampleGetChannel.argtypes = [ctypes.c_ulong, ctypes.c_bool]
            self.bass.BASS_SampleGetChannel.restype = ctypes.c_ulong

            # BASS_ChannelSetAttribute(DWORD handle, DWORD attrib, float value)
            self.bass.BASS_ChannelSetAttribute.argtypes = [ctypes.c_ulong, ctypes.c_ulong, ctypes.c_float]
            self.bass.BASS_ChannelSetAttribute.restype = ctypes.c_bool

            # BASS_ChannelPlay(DWORD handle, BOOL restart)
            self.bass.BASS_ChannelPlay.argtypes = [ctypes.c_ulong, ctypes.c_bool]
            self.bass.BASS_ChannelPlay.restype = ctypes.c_bool

            # BASS_SampleFree(HSAMPLE handle)
            self.bass.BASS_SampleFree.argtypes = [ctypes.c_ulong]
            self.bass.BASS_SampleFree.restype = ctypes.c_bool

            # BASS_Free()
            self.bass.BASS_Free.argtypes = []
            self.bass.BASS_Free.restype = ctypes.c_bool

            # Initialize default sound device (-1) at 44100Hz
            ok = self.bass.BASS_Init(-1, 44100, 0, None, None)
            if not ok:
                error_func = getattr(self.bass, "BASS_ErrorGetCode", None)
                error_code = error_func() if error_func else 0
                # Error code 32 = BASS_ERROR_ALREADY (already initialized in this process)
                if error_code != 32:
                    logger.warning(f"BASS_Init failed with error code: {error_code}")
                    return

            self.available = True
            logger.info(f"BASS audio initialized successfully using {lib_path.name}")

        except Exception as e:
            logger.exception(f"Failed to load or initialize BASS library: {e}")
            self.available = False

    def _load_sound(self, name: str, filepath: Path):
        if not self.available or not filepath.exists():
            return

        try:
            full_path = str(filepath.resolve())
            if sys.platform == "win32":
                file_arg = ctypes.cast(ctypes.c_wchar_p(full_path), ctypes.c_void_p)
                flags = BASS_UNICODE | BASS_SAMPLE_OVER_POS
            else:
                file_arg = ctypes.cast(ctypes.c_char_p(full_path.encode("utf-8")), ctypes.c_void_p)
                flags = BASS_SAMPLE_OVER_POS

            # Allow 8 simultaneous polyphonic sound channels for rapid typing
            sample_handle = self.bass.BASS_SampleLoad(False, file_arg, 0, 0, 8, flags)
            if sample_handle:
                self.samples[name] = sample_handle
                logger.debug(f"Loaded BASS sample: {name}")
            else:
                logger.warning(f"Failed to load sample {name} from {filepath}")
        except Exception as e:
            logger.error(f"Error loading sound {name}: {e}")

    def _load_all_sounds(self):
        sounds_dir = BASE_DIR / "assets" / "sounds"
        self._load_sound("correct", sounds_dir / "correct.wav")
        self._load_sound("error", sounds_dir / "error.wav")
        self._load_sound("complete", sounds_dir / "complete.wav")

    def play(self, name: str):
        if not self.available:
            return

        is_enabled = self.settings.get("sound_effects", True)
        if not is_enabled:
            return

        sample_handle = self.samples.get(name)
        if not sample_handle:
            logger.debug(f"Sound '{name}' not loaded.")
            return

        try:
            channel = self.bass.BASS_SampleGetChannel(sample_handle, False)
            if channel:
                volume = max(0.0, min(1.0, self.settings.get("sound_volume", 70) / 100.0))
                self.bass.BASS_ChannelSetAttribute(channel, BASS_ATTRIB_VOL, volume)
                self.bass.BASS_ChannelPlay(channel, True)
                logger.debug(f"Playing sound: {name} at volume {volume}")
            else:
                logger.warning(f"Could not allocate channel for sound: {name}")
        except Exception as e:
            logger.error(f"Error playing sound '{name}': {e}")

    def stop_all(self):
        pass

    def __del__(self):
        if self.available and self.bass:
            try:
                for sample in self.samples.values():
                    self.bass.BASS_SampleFree(sample)
                self.bass.BASS_Free()
            except Exception:
                pass

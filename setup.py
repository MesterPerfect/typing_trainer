import sys
import os
import shutil
import re
from cx_Freeze import setup, Executable

def get_version():
    """Extracts the version directly from core/constants.py to avoid manual duplication."""
    constants_path = os.path.join("core", "constants.py")
    try:
        with open(constants_path, "r", encoding="utf-8") as f:
            content = f.read()
            match = re.search(r'^(?:APP_)?VERSION\s*=\s*[\'"]([^\'"]*)[\'"]', content, re.MULTILINE)
            if match:
                return match.group(1)
    except Exception as e:
        print(f"Warning: Could not read version from {constants_path}. {e}")
    
    return "1.0.0"

def get_platform_config():
    if sys.platform == "win32":
        return "gui", ".exe"
    return None, ""

def get_include_files():
    base_files = [("assets", "assets"), ("locales", "locales")]

    # Include UniversalSpeech strictly for Windows if present locally
    if sys.platform == "win32":
        if os.path.exists("UniversalSpeech"):
            base_files.append(("UniversalSpeech", "UniversalSpeech"))

    return base_files

def clean_unused_folders(build_dir):
    """
    Cleans up unused heavy Qt libraries, QML engines, WebEngine, and plugins
    to dramatically reduce the final application size (from ~400MB down to ~40-50MB).
    """
    pyside_dir = os.path.join(build_dir, "lib", "PySide6")
    if not os.path.exists(pyside_dir):
        return

    # 1. Remove unused directories
    unused_dirs = [
        os.path.join(pyside_dir, "Qt6", "translations"),
        os.path.join(pyside_dir, "translations"),
        os.path.join(pyside_dir, "qml"),
        os.path.join(pyside_dir, "plugins", "sqldrivers"),
        os.path.join(pyside_dir, "plugins", "assetimporters"),
        os.path.join(pyside_dir, "plugins", "designer"),
        os.path.join(pyside_dir, "plugins", "generic"),
        os.path.join(pyside_dir, "plugins", "geometryloaders"),
        os.path.join(pyside_dir, "plugins", "qmltooling"),
        os.path.join(pyside_dir, "plugins", "scenegraph"),
        os.path.join(pyside_dir, "plugins", "sensors"),
        os.path.join(pyside_dir, "plugins", "position"),
        os.path.join(pyside_dir, "plugins", "renderers"),
        os.path.join(pyside_dir, "plugins", "spatialaudio"),
        os.path.join(pyside_dir, "plugins", "texttospeech"),
        os.path.join(pyside_dir, "plugins", "virtualkeyboard"),
        os.path.join(pyside_dir, "plugins", "webview"),
        os.path.join(pyside_dir, "plugins", "multimedia"),
        os.path.join(pyside_dir, "plugins", "networkinformation"),
    ]

    for d in unused_dirs:
        if os.path.exists(d):
            try:
                shutil.rmtree(os.path.abspath(d))
                print(f"Cleaned up unused directory: {d}")
            except Exception as e:
                print(f"Error removing {d}: {e}")

    # 2. Whitelist of necessary Qt DLLs in lib/PySide6
    # With BASS handling audio, we no longer need QtMultimedia or FFmpeg binaries!
    needed_dll_prefixes = (
        "Qt6Core",
        "Qt6Gui",
        "Qt6Widgets",
        "pyside6.",
        "shiboken6.",
        "opengl32sw",
    )

    allowed_pyds = {
        "QtCore.pyd",
        "QtGui.pyd",
        "QtWidgets.pyd",
    }

    for item in os.listdir(pyside_dir):
        item_path = os.path.join(pyside_dir, item)
        if os.path.isfile(item_path):
            name_lower = item.lower()
            if name_lower.startswith("qt6") or name_lower.endswith(".dll") or name_lower.endswith(".pyd"):
                if item.endswith(".pyd"):
                    is_needed = item in allowed_pyds
                else:
                    is_needed = any(item.startswith(prefix) for prefix in needed_dll_prefixes)
                
                if not is_needed:
                    try:
                        os.remove(item_path)
                        print(f"Removed unused Qt DLL/PYD: {item}")
                    except Exception as e:
                        print(f"Error removing {item}: {e}")

def main():
    version = get_version()
    print(f"Building TypingTrainer Version: {version}")
    
    base, ext = get_platform_config()
    target_name = f"TypingTrainer{ext}"
    build_dir = os.path.join("dist", "TypingTrainer")
    include_files = get_include_files()

    build_exe_options = {
        "build_exe": build_dir,
        "optimize": 2,
        "include_files": include_files,
        "packages": ["app", "core", "models", "services", "ui", "utils"],
        "includes": [
            "PySide6.QtCore",
            "PySide6.QtWidgets",
            "PySide6.QtGui",
            "ssl",
            "urllib",
            "platformdirs",
            "packaging",
        ],
        "excludes": [
            "tkinter", "test", "setuptools", "pip", "numpy", "unittest",
            "PySide6.QtMultimedia", "PySide6.QtMultimediaWidgets", "PySide6.QtNetwork",
            "PySide6.QtWebEngineCore", "PySide6.QtWebEngineWidgets", "PySide6.QtWebEngineQuick",
            "PySide6.QtDesigner", "PySide6.QtQml", "PySide6.QtQuick", "PySide6.QtQuickWidgets",
            "PySide6.QtOpenGL", "PySide6.QtSql", "PySide6.QtSvg", "PySide6.QtXml",
            "PySide6.QtTest", "PySide6.QtPrintSupport", "PySide6.QtSensors",
            "PySide6.QtPositioning", "PySide6.QtBluetooth", "PySide6.Qt3DCore",
            "PySide6.Qt3DRender", "PySide6.Qt3DAnimation", "PySide6.QtPdf",
            "PySide6.QtPdfWidgets", "PySide6.QtVirtualKeyboard", "PySide6.QtRemoteObjects",
            "PySide6.QtScxml", "PySide6.QtStateMachine", "PySide6.QtCharts",
            "PySide6.QtSpatialAudio", "PySide6.QtLabsAnimation", "PySide6.QtLottie"
        ],
    }

    icon_path = os.path.join("assets", "icon.ico")
    icon_file = icon_path if sys.platform == "win32" and os.path.exists(icon_path) else None

    setup(
        name="TypingTrainer",
        version=version,
        description="TypingTrainer - Accessible Typing Tutor",
        author="tecwindow",
        options={"build_exe": build_exe_options},
        executables=[
            # 1. Main Application
            Executable(
                "main.py",
                base=base,
                target_name=target_name,
                icon=icon_file,
            ),
            # 2. Silent Background Updater
            Executable(
                "apply_update.py",
                base=base,
                target_name=f"apply_update{ext}",
            )
        ],
    )

    clean_unused_folders(build_dir)

if __name__ == "__main__":
    main()

import sys
import os
import shutil
import platform
from cx_Freeze import setup, Executable
from core.constants import ICON_FILE_ICO

def get_platform_config():
    """Determine platform-specific base and executable extension."""
    if sys.platform == "win32":
        # 'Win32GUI' hides the console window on Windows
        return "Win32GUI", ".exe"
    return None, ""

def get_include_files():
    """Return a list of files and folders to include in the build."""
    base_files = [("assets", "assets"), ("locales", "locales")]

    # Include UniversalSpeech strictly for Windows
    if sys.platform == "win32":
        # Adjust the path if UniversalSpeech is located elsewhere in your project
        if os.path.exists("UniversalSpeech"):
            base_files.append(("UniversalSpeech", "UniversalSpeech"))

    return base_files

def clean_unused_folders(build_dir):
    """Remove unnecessary PySide6 bloat to reduce the final build size."""
    folder_paths = [
        os.path.join(build_dir, "lib", "PySide6", "Qt6", "translations"),
        os.path.join(build_dir, "lib", "PySide6", "Qt6", "plugins", "multimedia"),
    ]

    for folder in folder_paths:
        try:
            if os.path.exists(folder):
                shutil.rmtree(os.path.abspath(folder))
                print(f"Cleaned up: {folder}")
        except Exception as e:
            print(f"Error removing {folder}: {e}")

def main():
    version = os.environ.get("APP_VERSION", "1.0.0")
    base, ext = get_platform_config()

    # Determine accurate OS name for the build directory
    if sys.platform == "win32":
        os_name = "Windows"
    elif sys.platform == "darwin":
        os_name = "macOS"
    else:
        os_name = "Linux"
        
    arch = platform.machine()  # e.g., 'AMD64', 'x86_64', or 'arm64'

    target_name = f"TypingTrainer{ext}"
    build_dir = f"build/TypingTrainer_{os_name}_{arch}_v{version}"

    include_files = get_include_files()

    build_exe_options = {
        "build_exe": build_dir,
        "optimize": 2,
        "include_files": include_files,
        "packages": ["app", "core", "models", "services", "ui", "utils"],
        "includes": ["PySide6.QtCore", "PySide6.QtWidgets", "PySide6.QtGui"],
        "excludes": ["tkinter", "test", "setuptools", "pip", "numpy", "unittest"],
    }

    setup(
        name="Typing Trainer",
        version=version,
        description="Accessible Typing Tutor",
        author="MesterPerfect",
        options={"build_exe": build_exe_options},
        executables=[
            Executable(
                "main.py",
                base=base,
                target_name=target_name,
                # Conditionally embed the icon file strictly for Windows (.exe)
                icon=(
                    str(ICON_FILE_ICO)
                    if sys.platform == "win32" and ICON_FILE_ICO.exists()
                    else None
                ),
            )
        ],
    )

    # Run post-build cleanup
    clean_unused_folders(build_dir)

if __name__ == "__main__":
    main()

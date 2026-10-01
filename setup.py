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
            # Searches for lines like: APP_VERSION = "1.0.0" or VERSION = '1.0.0'
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
    # Clean up Qt translations to reduce size, keeping multimedia plugins
    folder_paths = [
        os.path.join(build_dir, "lib", "PySide6", "Qt6", "translations"),
    ]

    for folder in folder_paths:
        try:
            if os.path.exists(folder):
                shutil.rmtree(os.path.abspath(folder))
                print(f"Cleaned up: {folder}")
        except Exception as e:
            print(f"Error removing {folder}: {e}")

def main():
    version = get_version()
    print(f"Building TypingTrainer Version: {version}")
    
    base, ext = get_platform_config()

    target_name = f"TypingTrainer{ext}"
    
    # Output directly to dist/TypingTrainer to match the Inno Setup script and packaging pipelines
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
            "PySide6.QtMultimedia",
            "ssl",
            "urllib",
            "platformdirs",
            "packaging",
        ],
        "excludes": [
            "tkinter", "test", "setuptools", "pip", "numpy", "unittest",
            "PySide6.QtNetwork", "PySide6.QtQml", "PySide6.QtQuick", 
            "PySide6.QtOpenGL", "PySide6.QtSql", "PySide6.QtSvg", 
            "PySide6.QtXml", "PySide6.QtTest", "PySide6.QtPrintSupport",
            "PySide6.QtSensors", "PySide6.QtPositioning", "PySide6.QtBluetooth"
        ],
    }

    # Define icon path
    icon_path = os.path.join("assets", "icon.ico")
    icon_file = icon_path if sys.platform == "win32" and os.path.exists(icon_path) else None

    setup(
        name="TypingTrainer",
        version=version,
        description="TypingTrainer - Accessible Typing Tutor",
        author="MesterPerfect",
        options={"build_exe": build_exe_options},
        executables=[
            # 1. The Main Application
            Executable(
                "main.py",
                base=base,
                target_name=target_name,
                icon=icon_file,
            ),
            # 2. The Silent Background Updater
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

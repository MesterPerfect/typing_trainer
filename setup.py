import sys
import os
import shutil
import platform
from cx_Freeze import setup, Executable

def get_platform_config():
    """ Determine platform-specific base and executable extension. """
    platform_name = sys.platform
    if platform_name == "win32":
        # 'gui' hides the console window on Windows
        return "gui", ".exe"
    return None, ""

def get_include_files():
    """ Return a list of files and folders to include in the build. """
    base_files = [
        ("assets", "assets"),
        ("locales", "locales")
    ]
    
    # Include UniversalSpeech strictly for Windows
    if sys.platform == "win32":
        # Adjust the path if UniversalSpeech is located elsewhere in your project
        if os.path.exists("UniversalSpeech"):
            base_files.append(("UniversalSpeech", "UniversalSpeech"))
            
    return base_files

def clean_unused_folders(build_dir):
    """ Remove unnecessary PyQt6 bloat to reduce the final build size. """
    folder_paths = [
        os.path.join(build_dir, "lib", "PyQt6", "Qt6", "translations"),
        os.path.join(build_dir, "lib", "PyQt6", "Qt6", "plugins", "multimedia")
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
    
    # Determine accurate OS and Architecture names
    os_name = "Windows" if sys.platform == "win32" else "Linux"
    arch = platform.machine() # e.g., 'AMD64' or 'x86_64'
    
    target_name = f"TypingTrainer{ext}"
    build_dir = f"build/TypingTrainer_{os_name}_{arch}_v{version}"

    include_files = get_include_files()
    
    build_exe_options = {
        "build_exe": build_dir,
        "optimize": 2,
        "include_files": include_files,
        "packages": ["app", "core", "models", "services", "ui", "utils"],
        "includes": ["PyQt6.QtCore", "PyQt6.QtWidgets", "PyQt6.QtGui"],
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
                # Uncomment the next line and add an icon if you have one
                # icon="assets/icon.ico" if sys.platform == "win32" else None,
            )
        ]
    )
    
    # Run post-build cleanup
    clean_unused_folders(build_dir)

if __name__ == "__main__":
    main()

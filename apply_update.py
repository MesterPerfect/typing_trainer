import sys
import os
import time
import shutil
import subprocess
import zipfile
import tarfile
import argparse

def extract_archive(archive_path, extract_to):
    """Extracts zip or tar.gz archives."""
    if archive_path.endswith('.zip'):
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    elif archive_path.endswith(('.tar.gz', '.tgz')):
        with tarfile.open(archive_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    else:
        raise ValueError("Unsupported archive format. Must be .zip or .tar.gz")

def main():
    parser = argparse.ArgumentParser(description="Typing Trainer Background Updater")
    parser.add_argument("--archive", required=True, help="Path to the downloaded update archive")
    parser.add_argument("--target", required=True, help="Path to the application installation folder")
    parser.add_argument("--exe", required=True, help="Name of the main executable to restart")
    args = parser.parse_args()

    # 1. Give the main application 2 seconds to completely terminate
    time.sleep(2)

    # 2. Create a temporary extraction folder next to the target
    temp_ext_dir = os.path.join(args.target, "_update_temp")
    os.makedirs(temp_ext_dir, exist_ok=True)
    
    try:
        # 3. Extract the downloaded archive
        extract_archive(args.archive, temp_ext_dir)

        # Handle the case where the archive contains a single root folder (e.g., TypingTrainer_v1.2/)
        extracted_items = os.listdir(temp_ext_dir)
        if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_ext_dir, extracted_items[0])):
            source_dir = os.path.join(temp_ext_dir, extracted_items[0])
        else:
            source_dir = temp_ext_dir

        # 4. Wait until the main executable is totally released by the OS
        target_exe_path = os.path.join(args.target, args.exe)
        retries = 10
        while retries > 0:
            try:
                # Try to open the file in append mode. If it fails, it's still running.
                if os.path.exists(target_exe_path):
                    with open(target_exe_path, 'a'): pass
                break
            except Exception:
                time.sleep(1)
                retries -= 1

        # 5. Overwrite the old files with the new ones (dirs_exist_ok requires Python 3.8+)
        shutil.copytree(source_dir, args.target, dirs_exist_ok=True)

    except Exception as e:
        # If updating fails, write to a basic crash log
        with open(os.path.join(args.target, "updater_crash.log"), "w") as f:
            f.write(f"Update failed: {e}")
    finally:
        # 6. Cleanup temporary extraction folder and downloaded archive
        shutil.rmtree(temp_ext_dir, ignore_errors=True)
        try:
            os.remove(args.archive)
        except:
            pass

    # 7. Restart the main application
    target_exe_path = os.path.join(args.target, args.exe)
    if os.path.exists(target_exe_path):
        # DETACHED_PROCESS on Windows, normal on Linux/Mac
        if sys.platform == "win32":
            subprocess.Popen([target_exe_path], creationflags=subprocess.DETACHED_PROCESS)
        else:
            subprocess.Popen([target_exe_path], start_new_session=True)

if __name__ == "__main__":
    main()

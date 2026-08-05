import os
import json
import urllib.request
import zipfile
import shutil
import tempfile

VERSION_FILE = "version.txt"

def get_local_version() -> str:
    """Reads the local version file, defaulting to 'V1' if missing."""
    if os.path.exists(VERSION_FILE):
        try:
            with open(VERSION_FILE, "r") as f:
                return f.read().strip()
        except Exception:
            pass
    return "V1"

def set_local_version(version: str):
    """Writes the current version to the local version file."""
    try:
        with open(VERSION_FILE, "w") as f:
            f.write(version.strip())
    except Exception as e:
        print(f"[Error] Failed to write local version file: {e}")

def check_and_perform_update() -> bool:
    """
    Fetches the Firebase config, compares remote version_note to local,
    and automatically downloads, extracts, and updates the application if different.

    Returns:
    - True if an update was performed, indicating the application should restart.
    - False if already up to date.
    """
    firebase_url = os.getenv("FIREBASE_URL")
    if not firebase_url:
        print("[Update] FIREBASE_URL env var not set. Skipping update check.")
        return False

    print("[Update] Checking for updates...")
    try:
        url = f"{firebase_url.rstrip('/')}/config.json"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print("[Update] Failed to fetch server config.")
                return False
            cfg = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"[Update] Error checking server config: {e}")
        return False

    remote_version = cfg.get("version_note", "V1").strip()
    download_url = cfg.get("download_url", "").strip()
    local_version = get_local_version()

    if not remote_version or not download_url:
        print("[Update] Invalid server configuration. Skipping auto-update.")
        return False

    if remote_version == local_version:
        print(f"[✓] Already running the latest version ({local_version}).")
        return False

    print(f"\n[Update] New version detected! Server: {remote_version} | Local: {local_version}")
    print(f"[Update] Downloading package from: {download_url}")

    try:
        # Create a temporary file to hold the downloaded ZIP
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
            tmp_path = tmp_file.name

        # Download using urllib
        req_download = urllib.request.Request(download_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req_download) as response, open(tmp_path, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        print("[Update] Extracting update files...")
        with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
            zip_ref.extractall(".")

        # Clean up temporary file
        try:
            os.remove(tmp_path)
        except Exception:
            pass

        # Update local version tracker
        set_local_version(remote_version)
        print(f"[✓] Auto-Update Complete! System successfully updated to {remote_version}.\n")
        return True
    except Exception as e:
        print(f"[Update Error] Automatic update failed: {e}")
        return False


def perform_troubleshoot():
    """
    Troubleshooter utility that clears out temporary folders, cache paths,
    and log directories to optimize emulator and bypass operation.
    """
    print("\n==================================================")
    print("      TROUBLESHOOT SYSTEM: REPAIR & CLEANUP       ")
    print("==================================================")

    # 1. Clean local temp folders
    temp_dir = tempfile.gettempdir()
    print(f"[*] Cleaning Windows App Temp directory: {temp_dir}")
    clean_directory_contents(temp_dir)

    # 2. Clean common Emulator Temporary Cache and Log Paths
    user_profile = os.environ.get("USERPROFILE", "")
    app_data = os.environ.get("APPDATA", "")
    local_app_data = os.environ.get("LOCALAPPDATA", "")

    paths_to_clean = [
        os.path.join(local_app_data, "Tencent"),
        os.path.join(app_data, "Tencent"),
        "C:\\ProgramData\\Tencent",
        "C:\\Temp",
        "C:\\Windows\\Prefetch",
        os.path.join(local_app_data, "BlueStacks"),
        os.path.join(local_app_data, "ChangZhi"),
        os.path.join(local_app_data, "ChangZhi2"),
    ]

    for path in paths_to_clean:
        if os.path.exists(path):
            print(f"[*] Cleaning emulator path: {path}")
            clean_directory_contents(path)

    # 3. Clean local generator artifact caches
    local_cached_files = ["test_protos.json", "detailed_protos.json", "generated_protos.json"]
    for f in local_cached_files:
        if os.path.exists(f):
            try:
                os.remove(f)
                print(f"[*] Removed stale cache file: {f}")
            except Exception:
                pass

    print("\n[✓] Troubleshoot complete! Emulator caches cleared and system reset successfully!")
    print("==================================================\n")


def clean_directory_contents(dir_path: str):
    """Safely cleans the contents of a directory without deleting the directory itself."""
    if not os.path.exists(dir_path):
        return
    for item in os.listdir(dir_path):
        item_path = os.path.join(dir_path, item)
        try:
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
        except Exception:
            pass

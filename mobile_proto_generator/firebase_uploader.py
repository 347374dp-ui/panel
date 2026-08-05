import json
import time
import os
import urllib.request
import urllib.error

# Default database URL for ease of use
DEFAULT_FIREBASE_URL = "https://dipesh-database-default-rtdb.firebaseio.com"

def upload_proto_to_firebase(hex_str: str, firebase_url: str = None, auth_token: str = None) -> bool:
    """
    Uploads a mobile proto hex string to the Firebase database under /protos/{timestamp}.json.

    Parameters:
    - hex_str: The serialized protobuf hex string.
    - firebase_url: Optional custom Firebase Realtime Database URL. If not provided, it will
                    use the FIREBASE_URL environment variable or fallback to the default URL.
    - auth_token: Optional Firebase Database Secret or Auth ID Token. If not provided, it will
                  be loaded from the FIREBASE_AUTH environment variable.
    """
    # 1. Resolve Firebase URL
    url_base = firebase_url or os.getenv("FIREBASE_URL") or DEFAULT_FIREBASE_URL
    url_base = url_base.rstrip('/')

    # 2. Resolve Auth Token / Secret
    token = auth_token or os.getenv("FIREBASE_AUTH")

    # 3. Generate timestamp-based key matching Javascript Date.now()
    key = str(int(time.time() * 1000))

    # 4. Formulate URL
    url = f"{url_base}/protos/{key}.json"
    if token:
        # Firebase Realtime Database REST API authentication uses an auth query parameter
        url += f"?auth={token}"

    # 5. Firebase expects JSON-encoded data.
    data_bytes = json.dumps(hex_str).encode('utf-8')

    req = urllib.request.Request(
        url,
        data=data_bytes,
        headers={"Content-Type": "application/json"},
        method="PUT"
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                return True
            else:
                print(f"[Firebase] Non-200 response status: {response.status}")
                return False
    except urllib.error.URLError as e:
        print(f"[Firebase] Connection/HTTP error occurred: {e}")
        return False
    except Exception as e:
        print(f"[Firebase] Unexpected error: {e}")
        return False

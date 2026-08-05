import argparse
import sys
import json
import os
import binascii

from generator import generate_device_profile, serialize_profile_to_proto
from firebase_uploader import upload_proto_to_firebase

# ASCII Art for a professional look
BANNER = """
==================================================
        MOBILE PROTO GENERATOR FOR PROXY
==================================================
  Generate valid, randomized mobile profiles and
  serialize them to Protobuf format for DP Panel.
==================================================
"""

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(
        description="Mobile Protobuf Hex String Generator and Firebase Uploader.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-c", "--count",
        type=int,
        default=1,
        help="Number of mobile proto hex strings to generate (default: 1)."
    )

    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Path to save the generated hex strings (as JSON)."
    )

    parser.add_argument(
        "-u", "--upload",
        action="store_true",
        help="Upload the generated hex strings directly to the DP Panel Firebase RTDB."
    )

    parser.add_argument(
        "-d", "--details",
        action="store_true",
        help="Print the full readable mobile device profile details along with the hex."
    )

    parser.add_argument(
        "--firebase-url",
        type=str,
        help="Custom Firebase Realtime Database URL (overrides FIREBASE_URL env var)."
    )

    parser.add_argument(
        "--firebase-auth",
        type=str,
        help="Firebase Auth token / Secret database key (overrides FIREBASE_AUTH env var)."
    )

    args = parser.parse_args()

    if args.count <= 0:
        print("[Error] Count must be a positive integer greater than 0.")
        sys.exit(1)

    print(f"[*] Generating {args.count} mobile proto(s)...")

    protos = []
    for i in range(args.count):
        profile = generate_device_profile()
        proto_bytes = serialize_profile_to_proto(profile)
        hex_str = binascii.hexlify(proto_bytes).decode('utf-8')

        protos.append({
            "index": i + 1,
            "hex": hex_str,
            "profile": profile
        })

    # Display results
    for p in protos:
        print(f"\n[Proto #{p['index']}]")
        print(f"Hex (length: {len(p['hex'])} chars):\n{p['hex']}")
        if args.details:
            print("Device Profile Details:")
            for k, v in p["profile"].items():
                print(f"  {k:15}: {v}")

    # Save to file if output specified
    if args.output:
        try:
            # We save as a list of hex strings or dictionary based on details
            to_save = [p["hex"] for p in protos] if not args.details else protos
            with open(args.output, "w") as f:
                json.dump(to_save, f, indent=2)
            print(f"\n[+] Saved {args.count} generated proto(s) to: {args.output}")
        except Exception as e:
            print(f"\n[Error] Failed to save output file: {e}")

    # Upload to Firebase if specified
    if args.upload:
        print("\n[*] Uploading generated proto(s) to DP Panel Firebase Database...")
        success_count = 0
        for p in protos:
            print(f"  -> Uploading Proto #{p['index']}...", end="")
            success = upload_proto_to_firebase(
                p["hex"],
                firebase_url=args.firebase_url,
                auth_token=args.firebase_auth
            )
            if success:
                print(" SUCCESS")
                success_count += 1
            else:
                print(" FAILED")
        print(f"[+] Firebase Upload Complete. Successfully uploaded {success_count}/{args.count} proto(s).")
        print("[i] These protos will now be active in the DP Admin Control Panel's Proto Pool.")

if __name__ == "__main__":
    main()

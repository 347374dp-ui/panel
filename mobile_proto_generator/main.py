import argparse
import sys
import json
import os
import binascii

from generator import (
    generate_device_profile,
    serialize_profile_to_proto,
    AES,
    decode_aes_key,
    filter_protobuf_fields,
    find_safe_wildcard_aob
)
from firebase_uploader import upload_proto_to_firebase
from certificate_generator import generate_ca_certificate
from client_updater import check_and_perform_update, perform_troubleshoot, get_local_version

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

    # 1. Run automatic update check upon startup to see if we need to reload
    local_ver = get_local_version()
    print(f"[*] Local System Version: {local_ver}")
    updated = check_and_perform_update()
    if updated:
        print("[!] System was updated to a newer version! Please restart the program.")
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="Mobile Protobuf Hex String Generator, Encryptor and Firebase Uploader.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    # Existing Generator Options
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

    # Advanced Security & AES Encryption Options
    parser.add_argument(
        "--aes-key",
        type=str,
        help="Optional encoded AES Key (Hex or Base64). If provided, protos will be AES-CBC encrypted."
    )

    parser.add_argument(
        "--aes-iv",
        type=str,
        help="Optional 16-character/hex IV for AES encryption (defaults to random IV)."
    )

    parser.add_argument(
        "--filter-fields",
        type=str,
        help="Comma-separated list of protobuf field numbers to keep (e.g. '1,2,7,9,13'). All others are filtered out."
    )

    # Troubleshoot & Cert Commands
    parser.add_argument(
        "--troubleshoot",
        action="store_true",
        help="Run repair system: deletes local temporary directories, caches and repair emulator paths."
    )

    parser.add_argument(
        "--generate-cert",
        action="store_true",
        help="Automatically generate a unique self-signed CA TLS/SSL Certificate and private key."
    )

    # AOB Signature Finder Commands
    parser.add_argument(
        "--aob-original",
        type=str,
        help="Original build byte sequence in hexadecimal (AOB) to find safe signatures."
    )

    parser.add_argument(
        "--aob-patched",
        type=str,
        help="Patched/updated build byte sequence in hexadecimal (AOB) to find safe signatures."
    )

    args = parser.parse_args()

    # 2. Execute Troubleshoot Command if specified
    if args.troubleshoot:
        perform_troubleshoot()
        sys.exit(0)

    # 3. Execute Certificate Generation if specified
    if args.generate_cert:
        generate_ca_certificate()
        sys.exit(0)

    # 4. Execute AOB Signature Scanner if specified
    if args.aob_original and args.aob_patched:
        print("[*] Running Safe AOB Signature Finder & Compare System...")
        res = find_safe_wildcard_aob(args.aob_original, args.aob_patched)
        if res.get("success"):
            print("\n==================================================")
            print("          SAFE WILDCARD SIGNATURE GENERATED       ")
            print("==================================================")
            print(f"Signature (Length: {res['length']} bytes):")
            print(f"{res['signature']}")
            print("--------------------------------------------------")
            print(f"Wildcards Replaced : {res['wildcards']} bytes")
            print(f"Wildcard Density   : {res['wildcard_density_percent']}%")
            print(f"Signature Quality  : {res['quality_score']}/100")
            print("==================================================\n")
        else:
            print(f"[Error] AOB scanning failed: {res.get('error')}")
        sys.exit(0)

    if args.count <= 0:
        print("[Error] Count must be a positive integer greater than 0.")
        sys.exit(1)

    # Parse Allowed Fields for Protobuf filter
    allowed_fields = None
    if args.filter_fields:
        try:
            allowed_fields = set(int(f.strip()) for f in args.filter_fields.split(","))
            print(f"[*] Enabled field filtering. Allowed Protobuf fields: {sorted(list(allowed_fields))}")
        except ValueError:
            print("[Error] Invalid format for --filter-fields. Use comma-separated integers.")
            sys.exit(1)

    # Parse AES Key & IV
    cipher = None
    iv_bytes = None
    if args.aes_key:
        try:
            raw_key = decode_aes_key(args.aes_key)
            cipher = AES(raw_key)
            print(f"[*] Enabled AES Encryption. Key Decoded (Hex): {binascii.hexlify(raw_key).decode('utf-8')}")

            # Resolve IV
            if args.aes_iv:
                iv_raw = args.aes_iv.strip()
                if len(iv_raw) == 32: # Hex encoded
                    iv_bytes = binascii.unhexlify(iv_raw)
                else:
                    iv_bytes = iv_raw.encode('utf-8')[:16].ljust(16, b'\x00')
            else:
                iv_bytes = os.urandom(16)
            print(f"[*] AES Initialization Vector (IV): {binascii.hexlify(iv_bytes).decode('utf-8')}")
        except Exception as e:
            print(f"[Error] AES Configuration failed: {e}")
            sys.exit(1)

    print(f"[*] Generating {args.count} mobile proto(s)...")

    protos = []
    for i in range(args.count):
        profile = generate_device_profile()
        proto_bytes = serialize_profile_to_proto(profile)

        # Apply Protobuf Field Filtering if requested
        if allowed_fields is not None:
            proto_bytes = filter_protobuf_fields(proto_bytes, allowed_fields)

        # Apply AES Encryption if requested
        if cipher is not None and iv_bytes is not None:
            encrypted_bytes = cipher.encrypt_cbc(proto_bytes, iv_bytes)
            proto_payload = iv_bytes + encrypted_bytes
        else:
            proto_payload = proto_bytes

        hex_str = binascii.hexlify(proto_payload).decode('utf-8')

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

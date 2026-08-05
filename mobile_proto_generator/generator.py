import random
import string
import binascii

# Direct, dependency-free protobuf encoding helpers
def encode_varint(value: int) -> bytes:
    """Encodes an integer into protobuf varint format."""
    if value < 0:
        # Two's complement for negative numbers (64-bit varint representation)
        value = (1 << 64) + value
    out = bytearray()
    while True:
        b = value & 0x7f
        value >>= 7
        if value > 0:
            out.append(b | 0x80)
        else:
            out.append(b)
            break
    return bytes(out)

def encode_key(field_number: int, wire_type: int) -> bytes:
    """Encodes field key: (field_number << 3) | wire_type."""
    return encode_varint((field_number << 3) | wire_type)

def encode_string(field_number: int, s: str) -> bytes:
    """Encodes a string field (wire type 2)."""
    encoded_str = s.encode('utf-8')
    key = encode_key(field_number, 2)
    length = encode_varint(len(encoded_str))
    return key + length + encoded_str

def encode_bytes(field_number: int, b: bytes) -> bytes:
    """Encodes a bytes field (wire type 2)."""
    key = encode_key(field_number, 2)
    length = encode_varint(len(b))
    return key + length + b

def encode_int32(field_number: int, val: int) -> bytes:
    """Encodes an int32 field (wire type 0)."""
    key = encode_key(field_number, 0)
    return key + encode_varint(val)

# Helper generators for random mobile identifiers
def random_hex(length: int) -> str:
    """Generates a random lowercase hex string of specified length."""
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def random_digits(length: int) -> str:
    """Generates a random digit-only string of specified length."""
    return ''.join(random.choice(string.digits) for _ in range(length))

def random_mac() -> str:
    """Generates a random valid MAC address."""
    # Usually locally administered/unicast (first octet has 2, 6, A, or E as least significant nibble)
    first_octet = random.choice(['02', '12', '22', '32', '42', '52', '62', '72', '82', '92', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2'])
    remaining = [random_hex(2) for _ in range(5)]
    return ":".join([first_octet] + remaining)

def random_imei() -> str:
    """Generates a random 15-digit valid IMEI using Luhn algorithm."""
    # Luhn algorithm:
    # Start with 14 random digits
    digits = [int(random.choice(string.digits)) for _ in range(14)]
    # Calculate checksum digit
    total = 0
    for i, d in enumerate(digits):
        if i % 2 == 1:
            d_double = d * 2
            total += (d_double // 10) + (d_double % 10)
        else:
            total += d
    check_digit = (10 - (total % 10)) % 10
    digits.append(check_digit)
    return "".join(map(str, digits))

# Realistic Mobile Device Templates (with newest flagship models)
DEVICE_TEMPLATES = [
    {
        "brand": "Google",
        "manufacturer": "Google",
        "models": [
            {"model": "Pixel 5", "product": "redfin", "device": "redfin", "board": "redfin", "hardware": "redfin", "sdks": [30, 31, 32]},
            {"model": "Pixel 6 Pro", "product": "raven", "device": "raven", "board": "raven", "hardware": "oriole", "sdks": [31, 32, 33]},
            {"model": "Pixel 7 Pro", "product": "cheetah", "device": "cheetah", "board": "cheetah", "hardware": "cheetah", "sdks": [33, 34]},
            {"model": "Pixel 8 Pro", "product": "husky", "device": "husky", "board": "husky", "hardware": "husky", "sdks": [34]},
            {"model": "Pixel 9 Pro XL", "product": "komodo", "device": "komodo", "board": "komodo", "hardware": "komodo", "sdks": [34, 35]}
        ],
        "fingerprint_format": "google/{product}/{device}:{sdk}/{build_id}/{incremental}:user/release-keys",
        "build_id_formats": ["RQ3A.{date}.00{num}", "SQ3A.{date}.00{num}", "TQ3A.{date}.00{num}", "UQ1A.{date}.00{num}", "AP1A.{date}.00{num}"],
        "incremental_format": "8808{num}"
    },
    {
        "brand": "Samsung",
        "manufacturer": "Samsung",
        "models": [
            {"model": "Galaxy S20 Ultra", "product": "xyz123", "device": "xyz123", "board": "exynos990", "hardware": "samsungexynos990", "sdks": [29, 30, 31]},
            {"model": "Galaxy S21", "product": "o1q", "device": "o1q", "board": "lahaina", "hardware": "qcom", "sdks": [30, 31, 32]},
            {"model": "Galaxy S22 Ultra", "product": "b0q", "device": "b0q", "board": "taro", "hardware": "qcom", "sdks": [31, 32, 33]},
            {"model": "Galaxy S23 Ultra", "product": "dm3q", "device": "dm3q", "board": "kalama", "hardware": "qcom", "sdks": [33, 34]},
            {"model": "Galaxy S24 Ultra", "product": "e3q", "device": "e3q", "board": "pineapple", "hardware": "qcom", "sdks": [34]}
        ],
        "fingerprint_format": "samsung/{product}/{device}:{sdk}/{build_id}/{incremental}:user/release-keys",
        "build_id_formats": ["QP1A.{date}.0{num}", "SP1A.{date}.0{num}", "TP1A.{date}.0{num}", "UP1A.{date}.0{num}", "UP1A.{date}.0{num}"],
        "incremental_format": "G998BXXU5C{num}"
    },
    {
        "brand": "Xiaomi",
        "manufacturer": "Xiaomi",
        "models": [
            {"model": "Redmi Note 10", "product": "sunny", "device": "sunny", "board": "mojito", "hardware": "qcom", "sdks": [30, 31]},
            {"model": "Mi 11", "product": "venus", "device": "venus", "board": "venus", "hardware": "qcom", "sdks": [30, 31, 32]},
            {"model": "POCO F3", "product": "alioth", "device": "alioth", "board": "alioth", "hardware": "qcom", "sdks": [30, 31, 32, 33]},
            {"model": "Xiaomi 14 Ultra", "product": "aurora", "device": "aurora", "board": "pineapple", "hardware": "qcom", "sdks": [34]}
        ],
        "fingerprint_format": "xiaomi/{product}/{device}:{sdk}/{build_id}/{incremental}:user/release-keys",
        "build_id_formats": ["RKQ1.{date}.001", "SKQ1.{date}.001", "TKQ1.{date}.001", "UKQ1.{date}.001"],
        "incremental_format": "V13.0.{num}.0.SKIMIXM"
    },
    {
        "brand": "OnePlus",
        "manufacturer": "OnePlus",
        "models": [
            {"model": "OnePlus 9 Pro", "product": "OnePlus9Pro", "device": "OnePlus9Pro", "board": "lahaina", "hardware": "qcom", "sdks": [30, 31, 32]},
            {"model": "OnePlus 10 Pro", "product": "OnePlus10Pro", "device": "OnePlus10Pro", "board": "taro", "hardware": "qcom", "sdks": [32, 33]},
            {"model": "OnePlus 12", "product": "OnePlus12", "device": "OnePlus12", "board": "pineapple", "hardware": "qcom", "sdks": [34]}
        ],
        "fingerprint_format": "oneplus/{product}/{device}:{sdk}/{build_id}/{incremental}:user/release-keys",
        "build_id_formats": ["RKQ1.{date}.001", "SKQ1.{date}.001", "TKQ1.{date}.001", "UKQ1.{date}.001"],
        "incremental_format": "A.0{num}_20220{num}"
    }
]

def generate_device_profile() -> dict:
    """Generates a highly realistic, randomized Android device profile dictionary."""
    brand_tmpl = random.choice(DEVICE_TEMPLATES)
    model_tmpl = random.choice(brand_tmpl["models"])

    sdk = random.choice(model_tmpl["sdks"])

    # Generate realistic build date/numbers
    date_str = f"{random.randint(21, 24):02d}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
    num_str = f"{random.randint(1, 9)}"
    build_format = random.choice(brand_tmpl["build_id_formats"])
    build_id = build_format.format(date=date_str, num=num_str)

    inc_num = f"{random.randint(100, 999)}"
    incremental = brand_tmpl["incremental_format"].format(num=inc_num)

    # Fill format
    fingerprint = brand_tmpl["fingerprint_format"].format(
        product=model_tmpl["product"],
        device=model_tmpl["device"],
        sdk=sdk,
        build_id=build_id,
        incremental=incremental
    )

    profile = {
        "brand": brand_tmpl["brand"],
        "manufacturer": brand_tmpl["manufacturer"],
        "model": model_tmpl["model"],
        "product": model_tmpl["product"],
        "device": model_tmpl["device"],
        "board": model_tmpl["board"],
        "hardware": model_tmpl["hardware"],
        "sdk_version": sdk,
        "build_id": build_id,
        "incremental": incremental,
        "fingerprint": fingerprint,
        "android_id": random_hex(16),
        "mac_address": random_mac(),
        "imei": random_imei(),
        "serial_number": random_hex(12).upper()
    }
    return profile

def serialize_profile_to_proto(profile: dict) -> bytes:
    """Serializes a device profile into a binary Protobuf message."""
    # We serialize each field with its designated field number:
    # Field 1: brand
    # Field 2: model
    # Field 3: product
    # Field 4: device
    # Field 5: board
    # Field 6: manufacturer
    # Field 7: fingerprint
    # Field 8: hardware
    # Field 9: android_id
    # Field 10: mac_address
    # Field 11: imei
    # Field 12: serial_number
    # Field 13: sdk_version
    # Field 14: incremental
    # Field 15: build_id

    encoded = b""
    encoded += encode_string(1, profile["brand"])
    encoded += encode_string(2, profile["model"])
    encoded += encode_string(3, profile["product"])
    encoded += encode_string(4, profile["device"])
    encoded += encode_string(5, profile["board"])
    encoded += encode_string(6, profile["manufacturer"])
    encoded += encode_string(7, profile["fingerprint"])
    encoded += encode_string(8, profile["hardware"])
    encoded += encode_string(9, profile["android_id"])
    encoded += encode_string(10, profile["mac_address"])
    encoded += encode_string(11, profile["imei"])
    encoded += encode_string(12, profile["serial_number"])
    encoded += encode_int32(13, profile["sdk_version"])
    encoded += encode_string(14, profile["incremental"])
    encoded += encode_string(15, profile["build_id"])
    return encoded

def generate_mobile_proto_hex() -> str:
    """Generates a complete, new, valid mobile proto hex string."""
    profile = generate_device_profile()
    proto_bytes = serialize_profile_to_proto(profile)
    return binascii.hexlify(proto_bytes).decode('utf-8')

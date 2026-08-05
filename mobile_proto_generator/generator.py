import random
import string
import binascii
import base64
import time

# =====================================================================
# 1. PURE PYTHON AES IMPLEMENTATION (No external libraries required!)
# =====================================================================
class AES:
    """
    An elegant, dependency-free, pure-Python AES implementation.
    Supports AES-128, AES-192, and AES-256 encryption & decryption in CBC mode.
    """
    s_box = (
        0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
        0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
        0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
        0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
        0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
        0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
        0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
        0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
        0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
        0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
        0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
        0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
        0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
        0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
        0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
        0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
    )

    inv_s_box = (
        0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
        0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
        0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
        0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
        0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
        0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
        0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
        0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
        0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
        0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
        0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
        0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
        0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
        0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
        0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
        0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
    )

    r_con = (
        0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36
    )

    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 16, 24, or 32 bytes long.")
        self.key = key
        self.rounds = len(key) // 4 + 6
        self.round_keys = self._expand_key()

    def _sub_word(self, word: list) -> list:
        return [self.s_box[b] for b in word]

    def _rot_word(self, word: list) -> list:
        return word[1:] + word[:1]

    def _expand_key(self) -> list:
        key_words = []
        nk = len(self.key) // 4
        for i in range(nk):
            key_words.append([self.key[4*i], self.key[4*i+1], self.key[4*i+2], self.key[4*i+3]])

        for i in range(nk, 4 * (self.rounds + 1)):
            temp = key_words[i - 1][:]
            if i % nk == 0:
                temp = self._sub_word(self._rot_word(temp))
                temp[0] ^= self.r_con[i // nk]
            elif nk > 6 and i % nk == 4:
                temp = self._sub_word(temp)

            word = []
            for j in range(4):
                word.append(key_words[i - nk][j] ^ temp[j])
            key_words.append(word)
        return key_words

    def _add_round_key(self, state: list, round_idx: int):
        for i in range(4):
            for j in range(4):
                state[j][i] ^= self.round_keys[round_idx * 4 + i][j]

    def _sub_bytes(self, state: list):
        for i in range(4):
            for j in range(4):
                state[i][j] = self.s_box[state[i][j]]

    def _inv_sub_bytes(self, state: list):
        for i in range(4):
            for j in range(4):
                state[i][j] = self.inv_s_box[state[i][j]]

    def _shift_rows(self, state: list):
        state[1] = state[1][1:] + state[1][:1]
        state[2] = state[2][2:] + state[2][:2]
        state[3] = state[3][3:] + state[3][:3]

    def _inv_shift_rows(self, state: list):
        state[1] = state[1][-1:] + state[1][:-1]
        state[2] = state[2][-2:] + state[2][:-2]
        state[3] = state[3][-3:] + state[3][:-3]

    @staticmethod
    def xtime(a: int) -> int:
        return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1) & 0xFF

    @classmethod
    def mul_by_val(cls, x: int, y: int) -> int:
        res = 0
        for _ in range(8):
            if y & 1:
                res ^= x
            x = cls.xtime(x)
            y >>= 1
        return res

    def _mix_columns(self, state: list):
        for i in range(4):
            s0 = state[0][i]
            s1 = state[1][i]
            s2 = state[2][i]
            s3 = state[3][i]
            state[0][i] = self.xtime(s0) ^ (self.xtime(s1) ^ s1) ^ s2 ^ s3
            state[1][i] = s0 ^ self.xtime(s1) ^ (self.xtime(s2) ^ s2) ^ s3
            state[2][i] = s0 ^ s1 ^ self.xtime(s2) ^ (self.xtime(s3) ^ s3)
            state[3][i] = (self.xtime(s0) ^ s0) ^ s1 ^ s2 ^ self.xtime(s3)

    def _inv_mix_columns(self, state: list):
        for i in range(4):
            s0 = state[0][i]
            s1 = state[1][i]
            s2 = state[2][i]
            s3 = state[3][i]
            state[0][i] = self.mul_by_val(s0, 0x0e) ^ self.mul_by_val(s1, 0x0b) ^ self.mul_by_val(s2, 0x0d) ^ self.mul_by_val(s3, 0x09)
            state[1][i] = self.mul_by_val(s0, 0x09) ^ self.mul_by_val(s1, 0x0e) ^ self.mul_by_val(s2, 0x0b) ^ self.mul_by_val(s3, 0x0d)
            state[2][i] = self.mul_by_val(s0, 0x0d) ^ self.mul_by_val(s1, 0x09) ^ self.mul_by_val(s2, 0x0e) ^ self.mul_by_val(s3, 0x0b)
            state[3][i] = self.mul_by_val(s0, 0x0b) ^ self.mul_by_val(s1, 0x0d) ^ self.mul_by_val(s2, 0x09) ^ self.mul_by_val(s3, 0x0e)

    def _encrypt_block(self, block: bytes) -> bytes:
        state = [[block[i + 4*j] for j in range(4)] for i in range(4)]
        self._add_round_key(state, 0)

        for r in range(1, self.rounds):
            self._sub_bytes(state)
            self._shift_rows(state)
            self._mix_columns(state)
            self._add_round_key(state, r)

        self._sub_bytes(state)
        self._shift_rows(state)
        self._add_round_key(state, self.rounds)

        out = bytearray(16)
        for i in range(4):
            for j in range(4):
                out[i + 4*j] = state[i][j]
        return bytes(out)

    def _decrypt_block(self, block: bytes) -> bytes:
        state = [[block[i + 4*j] for j in range(4)] for i in range(4)]
        self._add_round_key(state, self.rounds)

        for r in range(self.rounds - 1, 0, -1):
            self._inv_shift_rows(state)
            self._inv_sub_bytes(state)
            self._add_round_key(state, r)
            self._inv_mix_columns(state)

        self._inv_shift_rows(state)
        self._inv_sub_bytes(state)
        self._add_round_key(state, 0)

        out = bytearray(16)
        for i in range(4):
            for j in range(4):
                out[i + 4*j] = state[i][j]
        return bytes(out)

    def encrypt_cbc(self, plaintext: bytes, iv: bytes) -> bytes:
        """Encrypts data in CBC mode with PKCS#7 padding."""
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes long.")
        pad_len = 16 - (len(plaintext) % 16)
        plaintext += bytes([pad_len] * pad_len)

        ciphertext = bytearray()
        prev_block = iv
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i+16]
            xor_block = bytes(b1 ^ b2 for b1, b2 in zip(block, prev_block))
            encrypted_block = self._encrypt_block(xor_block)
            ciphertext.extend(encrypted_block)
            prev_block = encrypted_block
        return bytes(ciphertext)

    def decrypt_cbc(self, ciphertext: bytes, iv: bytes) -> bytes:
        """Decrypts data in CBC mode and strips PKCS#7 padding."""
        if len(iv) != 16:
            raise ValueError("IV must be 16 bytes long.")
        if len(ciphertext) % 16 != 0:
            raise ValueError("Ciphertext length must be a multiple of 16.")

        plaintext = bytearray()
        prev_block = iv
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i+16]
            decrypted_block = self._decrypt_block(block)
            plain_block = bytes(b1 ^ b2 for b1, b2 in zip(decrypted_block, prev_block))
            plaintext.extend(plain_block)
            prev_block = block

        pad_len = plaintext[-1]
        if pad_len < 1 or pad_len > 16:
            return bytes(plaintext)
        for i in range(len(plaintext) - pad_len, len(plaintext)):
            if plaintext[i] != pad_len:
                return bytes(plaintext)
        return bytes(plaintext[:-pad_len])


# Helper for decoding encoded/obfuscated keys
def decode_aes_key(encoded_key: str) -> bytes:
    """
    Decodes an encoded AES key to raw bytes.
    Supports: Base64 encoding, URL-Safe Base64, raw hexadecimal.
    """
    cleaned = encoded_key.strip()

    if all(c in string.hexdigits for c in cleaned) and len(cleaned) in (32, 48, 64):
        try:
            return binascii.unhexlify(cleaned)
        except Exception:
            pass

    try:
        missing_padding = len(cleaned) % 4
        if missing_padding:
            cleaned += '=' * (4 - missing_padding)
        return base64.b64decode(cleaned.encode('utf-8'))
    except Exception:
        pass

    return cleaned.encode('utf-8')[:32].ljust(16, b'\x00')


# =====================================================================
# 2. DIRECT PROTOBUF ENCODING & PARSING ENGINE
# =====================================================================
def encode_varint(value: int) -> bytes:
    """Encodes an integer into protobuf varint format."""
    if value < 0:
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

def decode_varint(data: bytes, pos: int):
    """Decodes a protobuf varint starting at the given position."""
    val = 0
    shift = 0
    while True:
        if pos >= len(data):
            return None, pos
        b = data[pos]
        pos += 1
        val |= (b & 0x7f) << shift
        if not (b & 0x80):
            break
        shift += 7
    return val, pos

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


# =====================================================================
# 3. PROTOBUF FIELD PARSER AND BUILDER
# =====================================================================
def parse_protobuf_generic(proto_bytes: bytes) -> dict:
    """
    Parses any serialized protobuf bytes into a generic key-value dictionary.
    Structure: {"field_number": {"wire_type": "...", "data": ...}}
    """
    pos = 0
    fields = {}

    while pos < len(proto_bytes):
        start_pos = pos
        key, pos = decode_varint(proto_bytes, pos)
        if key is None:
            break

        wire_type = key & 0x7
        field_num = key >> 3

        if wire_type == 0:  # Varint
            val, pos = decode_varint(proto_bytes, pos)
            if val is None:
                break
            fields[str(field_num)] = {"wire_type": "varint", "data": val}

        elif wire_type == 1:  # 64-bit
            if pos + 8 > len(proto_bytes):
                break
            val_bytes = proto_bytes[pos:pos+8]
            pos += 8
            fields[str(field_num)] = {"wire_type": "64bit", "data": val_bytes}

        elif wire_type == 2:  # Length-delimited
            length, pos = decode_varint(proto_bytes, pos)
            if length is None or pos + length > len(proto_bytes):
                break
            sub_bytes = proto_bytes[pos:pos+length]
            pos += length

            try:
                val_str = sub_bytes.decode('utf-8')
                if any(c not in string.printable for c in val_str):
                    fields[str(field_num)] = {"wire_type": "bytes", "data": sub_bytes}
                else:
                    fields[str(field_num)] = {"wire_type": "string", "data": val_str}
            except UnicodeDecodeError:
                fields[str(field_num)] = {"wire_type": "bytes", "data": sub_bytes}

        elif wire_type == 5:  # 32-bit
            if pos + 4 > len(proto_bytes):
                break
            val_bytes = proto_bytes[pos:pos+4]
            pos += 4
            fields[str(field_num)] = {"wire_type": "32bit", "data": val_bytes}
        else:
            break

    return fields


def rebuild_protobuf_generic(fields: dict) -> bytes:
    """
    Reconstructs a serialized Protobuf byte payload from a generic key-value dictionary.
    """
    out = bytearray()
    for k in sorted(fields.keys(), key=int):
        field_num = int(k)
        entry = fields[k]
        wire_type = entry.get("wire_type")
        val = entry.get("data")

        if wire_type == "varint":
            out.extend(encode_key(field_num, 0))
            out.extend(encode_varint(int(val)))
        elif wire_type in ("string", "bytes"):
            out.extend(encode_key(field_num, 2))
            if isinstance(val, str):
                val_bytes = val.encode('utf-8')
            else:
                val_bytes = bytes(val)
            out.extend(encode_varint(len(val_bytes)))
            out.extend(val_bytes)
        elif wire_type in ("64bit", "32bit"):
            wt = 1 if wire_type == "64bit" else 5
            out.extend(encode_key(field_num, wt))
            out.extend(bytes(val))
    return bytes(out)


def filter_protobuf_fields(proto_bytes: bytes, allowed_field_numbers: set) -> bytes:
    """
    Parses serialized protobuf bytes and filters out any fields
    whose field numbers are NOT in the allowed_field_numbers set.
    """
    fields = parse_protobuf_generic(proto_bytes)
    filtered = {k: v for k, v in fields.items() if int(k) in allowed_field_numbers}
    return rebuild_protobuf_generic(filtered)


# =====================================================================
# 4. AOB SIGNATURE SCANNING & COMPARE UTILITY
# =====================================================================
def find_safe_wildcard_aob(original_hex: str, patched_hex: str) -> dict:
    """
    Compares two raw hex string byte sequences (from old and patched builds).
    Returns a unique wildcard AOB signature to ensure the bypass stays undetected/unpatched.
    """
    orig_clean = original_hex.strip().replace(" ", "")
    patch_clean = patched_hex.strip().replace(" ", "")

    try:
        orig_bytes = binascii.unhexlify(orig_clean)
        patch_bytes = binascii.unhexlify(patch_clean)
    except Exception as e:
        return {"success": False, "error": f"Invalid hex input bytes: {e}"}

    length = min(len(orig_bytes), len(patch_bytes))
    if length == 0:
        return {"success": False, "error": "Input bytes sequence is empty."}

    aob_parts = []
    wildcards_count = 0

    for i in range(length):
        b_orig = orig_bytes[i]
        b_patch = patch_bytes[i]
        if b_orig == b_patch:
            aob_parts.append(f"{b_orig:02X}")
        else:
            aob_parts.append("??")
            wildcards_count += 1

    aob_sig = " ".join(aob_parts)
    wildcard_density = (wildcards_count / length) * 100 if length > 0 else 0

    return {
        "success": True,
        "signature": aob_sig,
        "length": length,
        "wildcards": wildcards_count,
        "wildcard_density_percent": round(wildcard_density, 2),
        "quality_score": round(100 - wildcard_density, 1)
    }


# =====================================================================
# 5. RANDOM MOBILE IDENTIFIERS GENERATOR
# =====================================================================
def random_hex(length: int) -> str:
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))

def random_digits(length: int) -> str:
    return ''.join(random.choice(string.digits) for _ in range(length))

def random_mac() -> str:
    first_octet = random.choice(['02', '12', '22', '32', '42', '52', '62', '72', '82', '92', 'a2', 'b2', 'c2', 'd2', 'e2', 'f2'])
    remaining = [random_hex(2) for _ in range(5)]
    return ":".join([first_octet] + remaining)

def random_imei() -> str:
    digits = [int(random.choice(string.digits)) for _ in range(14)]
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


# =====================================================================
# 6. REALISTIC MOBILE DEVICE TEMPLATES
# =====================================================================
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
        "incremental_format": "8808{num}",
        "gpu": "Google Tensor GPU",
        "gles": "OpenGL ES 3.2 Google GPU"
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
        "build_id_formats": ["QP1A.{date}.0{num}", "SP1A.{date}.0{num}", "TP1A.{date}.0{num}", "UP1A.{date}.0{num}"],
        "incremental_format": "G998BXXU5C{num}",
        "gpu": "Adreno (TM) 750",
        "gles": "OpenGL ES 3.2 V@0615.0 (GIT@777ca53, I5e0e0fb907, 1638827725)"
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
        "incremental_format": "V13.0.{num}.0.SKIMIXM",
        "gpu": "Adreno (TM) 750",
        "gles": "OpenGL ES 3.2 V@0615.0"
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
        "incremental_format": "A.0{num}_20220{num}",
        "gpu": "Adreno (TM) 750",
        "gles": "OpenGL ES 3.2 V@0615.0"
    }
]

def generate_device_profile() -> dict:
    brand_tmpl = random.choice(DEVICE_TEMPLATES)
    model_tmpl = random.choice(brand_tmpl["models"])

    sdk = random.choice(model_tmpl["sdks"])

    date_str = f"{random.randint(21, 24):02d}{random.randint(1, 12):02d}{random.randint(1, 28):02d}"
    num_str = f"{random.randint(1, 9)}"
    build_format = random.choice(brand_tmpl["build_id_formats"])
    build_id = build_format.format(date=date_str, num=num_str)

    inc_num = f"{random.randint(100, 999)}"
    incremental = brand_tmpl["incremental_format"].format(num=inc_num)

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
        "board": brand_tmpl["board"] if "board" in brand_tmpl else model_tmpl["board"],
        "hardware": model_tmpl["hardware"],
        "sdk_version": sdk,
        "build_id": build_id,
        "incremental": incremental,
        "fingerprint": fingerprint,
        "android_id": random_hex(16),
        "mac_address": random_mac(),
        "imei": random_imei(),
        "serial_number": random_hex(12).upper(),
        "gpu": brand_tmpl.get("gpu", "Adreno (TM) 730"),
        "gles": brand_tmpl.get("gles", "OpenGL ES 3.2")
    }
    return profile

def serialize_profile_to_proto(profile: dict) -> bytes:
    """Serializes a device profile into a binary Protobuf message."""
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
    profile = generate_device_profile()
    proto_bytes = serialize_profile_to_proto(profile)
    return binascii.hexlify(proto_bytes).decode('utf-8')


# =====================================================================
# 7. SAFEV2 FULL-COMPATIBILITY RECONSTRUCTION LOGIC
# =====================================================================
# Matches the Base64 key and IV of safev2 exactly
SAFEV2_KEY = base64.b64decode("WWcmdGMlREV1aDYlWmNeOA==")
SAFEV2_IV = base64.b64decode("Nm95WkRyMjJFM3ljaGpNJQ==")

# Standard template payload extracted from safev2
SAFEV2_BASE_TEMPLATE = (
    "aaf8a186a5c94b33453a39cc44d8fdef5971fedbd4ddafda01d8705a9c3628ff74c00856c47b11bba56d76991f6e3830d9288e0836d47287dbb3f8d9070889f5ceb65e357973cb498a77f5fda5d3e98821fc5ade51433944f9d78538b8c4236419d8a87f13ee462a1b19fc5962c6521fe56f926173f45f6f299a328d7dfee9c2949ecb4c50e2051427f49c3a65e8b9f1dc2dd8c8dddc8dc8c31793f3846b5832fb0ca1ed3c49bdbcbfcf1b6b828c4bb60d101fcc8e4a3dc78c12bbc06040ac295e1064e568a922f1c374d6d26a0c7d6bafd58b7c1cf3fc4fa0de004756805b927aa6c25a135dccfb58c2e3eef66b3e22a81882be9942cb89cb9511072fb98e7dc76fdfc834f825e09c1447481b4ba6e5c0357aaf93406f46cc342fc3871e8e799a7fa64802664411d6a520a3e024ee59b616fb6888e8971dc8c15e6e3d41139855a7e10d6feeb5a12d0855a00795d10a8c1a2d1396b99c49a5fb6151bdbeb3be7515a67947719c04e1b1aa4b7e77ab5cc465c3d3a1993fb35910b9ce5264fe84ad2fd30b47f9a0514568ce19e62e036921be2be52e22d4f65828248557d83b269f728a618c48a82829a38b4dac90ec71dcaa353ef94312be097a704664603d533feb7a37cf8b6cf87c7c9d0ec4d6f53246dafd025628dcdfcc05b34e6eda532be29dcdfb45c1ab2c8a26ce84859d5006aa06d4c2138a9b8a2a52ec08a2fe68022cae61cd5192d02c4560926c9ef6f6c1033c8136c4dd2daad77657a02a8d7e0383772a85d7cae1a7ae1b08d5cf90afb615e473c3f72ab6155e242692799ce1e54c5355a68f79cb30a1d6b2a4eb6876a3de2173297c461f0d13a09e9745efe996e0080e679a34e828fb0ef04da2a409c4dc4918f515b0eae02bde4e82276c757f7dadfabb649486085ca943cfcc0b7eb10c0df238c6613f6da2dea5a7d18b0817a690de4ebc8f15445a43687433128d657a86d47a6c296ed1a35a092b9a06fe8dc54ba3888e1afab2fa502d443536bc74028df5de33ec4140dea370aa45a5132a8fa33fc3ba2f986cc8578b4d4a2e0e5f4615334329f1f43da573efc8ee8e7d6fb47de991bd7b16b1818484f6d0e489e676acbaf62300ecb1ead8dbc15ed2cdfeb98e7533e1306d5c89a129030650ee86bf0398d651e7cc59b934b871535ef432e3571a52d9cfcbbecb7b180a09bce53063e5449f6b6393c09d7e175aae7c599190bf39ade583251c8922b582e8a91bf261e9d678cac4c4e9aadbaf19aef7ca09edbf79e7884a23b3702c3bc4e3227e2c"
)

def generate_safev2_encrypted_proto() -> tuple:
    """
    Implements the exact same logic, steps, and cryptography of safev2:
    1. Decrypts the safev2 baseline template using SAFEV2_KEY and SAFEV2_IV.
    2. Parses the decrypted bytes into a generic fields dictionary.
    3. Generates a fully randomized new flagship mobile device profile (Samsung, Pixel, etc.).
    4. Overwrites the device specifications:
       - Field 3: Current local Timestamp
       - Field 8: Android Build/OS Info
       - Field 10: Manufacturer / Brand
       - Field 12: Width
       - Field 13: Height
       - Field 14: Screen Density
       - Field 17: GPU Renderer
       - Field 18: GLES Version info
       - Field 19: Product model string
       - Field 25: Device Model
    5. Re-serializes the fields back into standard Protobuf bytes.
    6. Re-encrypts the bytes with SAFEV2_KEY and SAFEV2_IV.
    7. Returns a tuple: (final_hex_string, randomized_device_profile)
    """
    # 1. Decrypt original template
    aes = AES(SAFEV2_KEY)
    decrypted_bytes = aes.decrypt_cbc(binascii.unhexlify(SAFEV2_BASE_TEMPLATE), SAFEV2_IV)

    # 2. Parse protobuf fields
    fields = parse_protobuf_generic(decrypted_bytes)

    # 3. Generate randomized device profile specs
    dev = generate_device_profile()

    # Current timestamp in exact "YYYY-MM-DD HH:MM:SS" format
    current_time_str = time.strftime("%Y-%m-%d %H:%M:%S")

    # Android OS string
    android_os_str = f"Android OS {dev['sdk_version']} / API-{dev['sdk_version']} ({dev['build_id']}/{random_digits(7)})"

    # 4. Map and overwrite fields
    fields["3"] = {"wire_type": "string", "data": current_time_str}
    fields["8"] = {"wire_type": "string", "data": android_os_str}
    fields["10"] = {"wire_type": "string", "data": dev["brand"].lower()}

    # Standard flagship resolutions
    width = 1440 if dev["brand"] == "Samsung" or dev["brand"] == "Google" else 1080
    height = 3120 if dev["brand"] == "Samsung" else (2400 if dev["brand"] == "Google" else 2160)
    density = "480" if dev["brand"] == "Samsung" or dev["brand"] == "Google" else "320"

    dev["width"] = width
    dev["height"] = height
    dev["density"] = density
    dev["timestamp"] = current_time_str
    dev["android_build_os"] = android_os_str

    fields["12"] = {"wire_type": "varint", "data": width}
    fields["13"] = {"wire_type": "varint", "data": height}
    fields["14"] = {"wire_type": "string", "data": density}

    fields["17"] = {"wire_type": "string", "data": dev["gpu"]}
    fields["18"] = {"wire_type": "string", "data": dev["gles"]}

    # Format of Field 19: "brand|uuid" or "brand|model"
    fields["19"] = {"wire_type": "string", "data": f"{dev['brand'].lower()}|{dev['model']}"}
    fields["25"] = {"wire_type": "string", "data": dev["model"]}

    # Randomize other unique identifiers to prevent system-fingerprinting
    fields["22"] = {"wire_type": "string", "data": random_hex(32)}
    fields["57"] = {"wire_type": "string", "data": random_hex(32)}

    # 5. Rebuild Protobuf bytes
    new_proto_bytes = rebuild_protobuf_generic(fields)

    # 6. Encrypt bytes
    encrypted_bytes = aes.encrypt_cbc(new_proto_bytes, SAFEV2_IV)

    # 7. Convert to hex string and return alongside the generated profile dictionary
    return encrypted_bytes.hex(), dev

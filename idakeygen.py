# -*- coding: utf-8 -*-

import json
import hashlib
import os
import platform
 
license = {
    "header": {"version": 1},
    "payload": {
        "name": "IDAPRO9",
        "email": "idapro9@example.com",
        "licenses": [
            {
                "id": "48-2137-ACAB-99",
                "edition_id": "ida-pro",
                "description": "license",
                "license_type": "named",
                "product": "IDA",
                "product_id": "IDAPRO",
                "product_version": "9.1",
                "seats": 1,
                "start_date": "2024-08-10 00:00:00",
                "end_date": "2033-12-31 23:59:59",
                "issued_on": "2024-08-10 00:00:00",
                "owner": "HexRays",
                "add_ons": [],
                "features": [],
            }
        ],
    },
}
 
def add_every_addon(license):
    platforms = [
        "W",  # Windows
        "L",  # Linux
        "M",  # macOS
    ]
    addons = [
        "HEXX86",
        "HEXX64",
        "HEXARM",
        "HEXARM64",
        "HEXMIPS",
        "HEXMIPS64",
        "HEXPPC",
        "HEXPPC64",
        "HEXRV64",
        "HEXARC",
        "HEXARC64",
    ]
 
    i = 0
    for addon in addons:
        i += 1
        license["payload"]["licenses"][0]["add_ons"].append(
            {
                "id": f"48-1337-0000-{i:02}",
                "code": addon,
                "owner": license["payload"]["licenses"][0]["id"],
                "start_date": "2024-08-10 00:00:00",
                "end_date": "2033-12-31 23:59:59",
            }
        )
    
add_every_addon(license)
 
def json_stringify_alphabetical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))
 
def buf_to_bigint(buf):
    return int.from_bytes(buf, byteorder="little")
 
def bigint_to_buf(i):
    return i.to_bytes((i.bit_length() + 7) // 8, byteorder="little")
 
# Yup, you only have to patch 5c -> cb in libida64.so
pub_modulus_hexrays = buf_to_bigint(
    bytes.fromhex(
        "edfd425cf978546e8911225884436c57140525650bcf6ebfe80edbc5fb1de68f4c66c29cb22eb668788afcb0abbb718044584b810f8970cddf227385f75d5dddd91d4f18937a08aa83b28c49d12dc92e7505bb38809e91bd0fbd2f2e6ab1d2e33c0c55d5bddd478ee8bf845fcef3c82b9d2929ecb71f4d1b3db96e3a8e7aaf93"
    )
)
pub_modulus_patched = buf_to_bigint(
    bytes.fromhex(
        "edfd42cbf978546e8911225884436c57140525650bcf6ebfe80edbc5fb1de68f4c66c29cb22eb668788afcb0abbb718044584b810f8970cddf227385f75d5dddd91d4f18937a08aa83b28c49d12dc92e7505bb38809e91bd0fbd2f2e6ab1d2e33c0c55d5bddd478ee8bf845fcef3c82b9d2929ecb71f4d1b3db96e3a8e7aaf93"
    )
)
 
private_key = buf_to_bigint(
    bytes.fromhex(
        "77c86abbb7f3bb134436797b68ff47beb1a5457816608dbfb72641814dd464dd640d711d5732d3017a1c4e63d835822f00a4eab619a2c4791cf33f9f57f9c2ae4d9eed9981e79ac9b8f8a411f68f25b9f0c05d04d11e22a3a0d8d4672b56a61f1532282ff4e4e74759e832b70e98b9d102d07e9fb9ba8d15810b144970029874"
    )
)
 
def decrypt(message):
    decrypted = pow(buf_to_bigint(message), exponent, pub_modulus_patched)
    decrypted = bigint_to_buf(decrypted)
    return decrypted[::-1]
 
def encrypt(message):
    encrypted = pow(buf_to_bigint(message[::-1]), private_key, pub_modulus_patched)
    encrypted = bigint_to_buf(encrypted)
    return encrypted
 
exponent = 0x13
 
def sign_hexlic(payload: dict) -> str:
    data = {"payload": payload}
    data_str = json_stringify_alphabetical(data)
 
    buffer = bytearray(128)
    # first 33 bytes are random
    for i in range(33):
        buffer[i] = 0x42
 
    # compute sha256 of the data
    sha256 = hashlib.sha256()
    sha256.update(data_str.encode())
    digest = sha256.digest()
 
    # copy the sha256 digest to the buffer
    for i in range(32):
        buffer[33 + i] = digest[i]
 
    # encrypt the buffer
    encrypted = encrypt(buffer)
 
    return encrypted.hex().upper()
 
def patch(filename):
    if not os.path.exists(filename):
        print(f"Skip: {filename} - didn't find")
        return
 
    with open(filename, "rb") as f:
        data = f.read()
 
        if data.find(bytes.fromhex("EDFD42CBF978")) != -1:
            print(f"Patch: {filename} - looks to be already patched :)")
            return
 
        if data.find(bytes.fromhex("EDFD425CF978")) == -1:
            print(f"Patch: {filename} - doesn't contain the original modulus.")
            return
 
        data = data.replace(
            bytes.fromhex("EDFD425CF978"), bytes.fromhex("EDFD42CBF978")
        )
     
    with open(filename, "wb") as f:
        f.write(data)

    print(f"Patch: {filename} - OK")
 
license["signature"] = sign_hexlic(license["payload"])
serialized = json_stringify_alphabetical(license)
 
filename = "idapro.hexlic"
with open(filename, "w") as f:
    f.write(serialized)
 
print(f"\nSaved new license to {filename}!\n")
 
os_name = platform.system().lower()
if os_name == 'windows':
    patch("ida.dll")
    patch("ida32.dll")
elif os_name == 'linux':
    patch("libida.so")
    patch("libida32.so")
elif os_name == 'darwin':
    patch("libida.dylib")
    patch("libida32.dylib")
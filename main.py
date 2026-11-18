#!/usr/bin/env python3
"""news-image-20261118 entry: emit the front page to /output/entry.png.

The picture is "The World in One Day" for Wednesday 18 November 2026,
drawn in code by render.py (PIL + DejaVu, no external assets) and stored
here as one line of base64 in entry.b64, because the grader's sandbox
has no network and the entry must be self-contained. This program only
decodes that payload, checks it is a whole 1024x1024 PNG under 1 MiB,
and writes it out. Two runs produce byte-identical output.

Run locally with:  MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import base64
import hashlib
import os
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
PAYLOAD = HERE / "entry.b64"
TARGET = OUT / "entry.png"


def png_size(data):
    """Read (width, height) from the IHDR chunk of a PNG, or None."""
    if len(data) < 33 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def png_is_whole(data):
    """True if the PNG ends with a proper IEND chunk (not truncated)."""
    if len(data) < 12 or data[-12:-8] != b"\x00\x00\x00\x00":
        return False
    return data[-8:-4] == b"IEND" and data[-4:] == b"\xaeB`\x82"


def main():
    encoded = PAYLOAD.read_text().strip()
    assert "\n" not in encoded and " " not in encoded, "entry.b64 must be one line"
    data = base64.b64decode(encoded, validate=True)
    assert len(data) <= 1_048_576, f"image too large: {len(data)} bytes"
    dims = png_size(data)
    assert dims == (1024, 1024), f"expected 1024x1024 PNG, got {dims}"
    assert png_is_whole(data), "PNG is truncated: no IEND chunk"
    OUT.mkdir(parents=True, exist_ok=True)
    tmp = TARGET.with_name(".entry.png.tmp")
    tmp.write_bytes(data)
    assert tmp.read_bytes() == data, "read-back mismatch, refusing to publish"
    os.replace(tmp, TARGET)
    print(f"entry.png: {len(data)} bytes, {dims[0]}x{dims[1]}, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")


if __name__ == "__main__":
    main()

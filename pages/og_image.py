"""Small PNG used for Open Graph / Twitter card previews (no extra dependencies)."""

from __future__ import annotations

import struct
import zlib


def _png_chunk(chunk_type: bytes, data: bytes) -> bytes:
    crc = zlib.crc32(chunk_type + data) & 0xFFFFFFFF
    return struct.pack(">I", len(data)) + chunk_type + data + struct.pack(">I", crc)


def _two_tone_rgb_png(width: int, height: int, top_rgb: tuple[int, int, int], bottom_rgb: tuple[int, int, int]) -> bytes:
    """RGB PNG, filter type 0 per scanline; horizontal split at two-thirds height."""
    signature = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    split_y = int(height * 2 / 3)
    raw = bytearray()
    tr, tg, tb = top_rgb
    br, bg, bb = bottom_rgb
    row_top = b"\x00" + bytes((tr, tg, tb)) * width
    row_bottom = b"\x00" + bytes((br, bg, bb)) * width
    for y in range(height):
        raw.extend(row_top if y < split_y else row_bottom)
    compressed = zlib.compress(bytes(raw), 9)
    return signature + _png_chunk(b"IHDR", ihdr) + _png_chunk(b"IDAT", compressed) + _png_chunk(b"IEND", b"")


# Brand paper + primary (matches CSS marketing palette).
OG_CARD_PNG = _two_tone_rgb_png(
    1200,
    630,
    top_rgb=(0xFA, 0xF8, 0xF1),
    bottom_rgb=(0x1F, 0x6F, 0x61),
)

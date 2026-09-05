"""以標準函式庫驗證可分發桌寵的 manifest、固定雜湊與無損 WebP 標頭。"""
from pathlib import Path
import hashlib
import json
import struct

ROOT = Path(__file__).resolve().parents[1]


def dimensions(data):
    if len(data) < 12 or data[:4] != b'RIFF' or data[8:12] != b'WEBP':
        raise ValueError('Invalid WebP RIFF header')
    if struct.unpack_from('<I', data, 4)[0] + 8 != len(data):
        raise ValueError('Truncated or extended RIFF data')
    offset = 12
    while offset + 8 <= len(data):
        kind = data[offset:offset + 4]
        size = struct.unpack_from('<I', data, offset + 4)[0]
        start, end = offset + 8, offset + 8 + size
        if end > len(data):
            raise ValueError('Truncated WebP chunk')
        if kind == b'VP8L':
            if size < 5 or data[start] != 0x2f:
                raise ValueError('Invalid lossless WebP signature')
            bits = struct.unpack_from('<I', data, start + 1)[0]
            return 1 + (bits & 0x3fff), 1 + ((bits >> 14) & 0x3fff)
        offset = end + (size & 1)
    raise ValueError('Expected a lossless VP8L atlas')


def verify(root=ROOT):
    manifest = json.loads((root / 'pet/pet.json').read_text(encoding='utf-8'))
    expected = {'id': 'deepseek-girl-codex-pet', 'spriteVersionNumber': 2,
                'spritesheetPath': 'spritesheet.webp'}
    for field, value in expected.items():
        if manifest.get(field) != value:
            raise ValueError(f'Unexpected {field}')
    rows = (root / 'SHA256SUMS').read_text(encoding='ascii').strip().splitlines()
    if len(rows) != 1:
        raise ValueError('Expected the single atlas checksum')
    digest, name = rows[0].split()
    if name != 'pet/spritesheet.webp':
        raise ValueError('Unexpected checksum path')
    atlas = (root / name).read_bytes()
    if hashlib.sha256(atlas).hexdigest() != digest:
        raise ValueError('Atlas SHA-256 mismatch')
    if dimensions(atlas) != (1536, 2288):
        raise ValueError('Unexpected atlas dimensions')
    return {'manifest': 'PASS', 'sha256': digest, 'dimensions': [1536, 2288],
            'scope': 'Package integrity; not a live Codex compatibility test'}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2))

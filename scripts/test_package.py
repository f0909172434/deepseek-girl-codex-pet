"""檔案損壞不能安裝；分發白名單與 ZIP metadata 必須可重複。"""
from pathlib import Path
import json
import shutil
import tempfile
import unittest
import zipfile
from verify import ROOT, dimensions, verify
from package import FILES, package


class PackageTests(unittest.TestCase):
    def test_repeated_build_and_extracted_package(self):
        path = package()
        first = path.read_bytes()
        self.assertEqual(first, package().read_bytes())
        with zipfile.ZipFile(path) as archive, tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(archive.namelist(), sorted(FILES))
            self.assertTrue(all(info.date_time == (2026, 1, 1, 0, 0, 0) for info in archive.infolist()))
            archive.extractall(tmp)
            verify(Path(tmp))

    def test_rejects_truncated_atlas(self):
        with self.assertRaises(ValueError):
            dimensions((ROOT / 'pet/spritesheet.webp').read_bytes()[:-10])

    def test_rejects_modified_bytes_and_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'pet', root / 'pet')
            shutil.copyfile(ROOT / 'SHA256SUMS', root / 'SHA256SUMS')
            atlas = root / 'pet/spritesheet.webp'
            original = atlas.read_bytes()
            atlas.write_bytes(original[:-1] + bytes([original[-1] ^ 1]))
            with self.assertRaisesRegex(ValueError, 'SHA-256'):
                verify(root)
            atlas.write_bytes(original)
            manifest = root / 'pet/pet.json'
            data = json.loads(manifest.read_text(encoding='utf-8'))
            data['spritesheetPath'] = '../outside.webp'
            manifest.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'spritesheetPath'):
                verify(root)


if __name__ == '__main__':
    unittest.main()

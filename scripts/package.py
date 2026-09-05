"""以排序白名單與固定 ZIP metadata 產生可重複的安裝包。"""
from pathlib import Path
import hashlib
import re
import zipfile
from verify import ROOT, verify

FILES = ['VERSION', 'README.md', 'LICENSE', 'RELEASE.md', 'SHA256SUMS',
         'pet/pet.json', 'pet/spritesheet.webp', 'scripts/install.ps1',
         'scripts/verify.ps1', 'scripts/verify.py', 'scripts/package.py',
         'scripts/test_package.py', 'scripts/test-install.ps1',
         'assets/contact-sheet.png', 'assets/deepseek-girl-in-codex.gif',
         'docs/assets/readme-hero.svg', 'qa/atlas-validation.json']


def package():
    verify()
    version = (ROOT / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('VERSION must be a release version')
    output = ROOT / 'dist'
    output.mkdir(exist_ok=True)
    path = output / f'deepseek-girl-codex-pet-{version}.zip'
    temporary = path.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(FILES):
            entry = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, (ROOT / name).read_bytes(), compresslevel=9)
    temporary.replace(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    (output / 'SHA256SUMS').write_text(f'{digest}  {path.name}\n', encoding='ascii')
    print(f'{digest}  {path.name}')
    return path


if __name__ == '__main__':
    package()

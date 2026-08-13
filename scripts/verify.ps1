$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PetDir = Join-Path $RepoRoot "pet"
$ManifestPath = Join-Path $PetDir "pet.json"
$AtlasPath = Join-Path $PetDir "spritesheet.webp"
$ChecksumPath = Join-Path $RepoRoot "SHA256SUMS"

$Manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
if ($Manifest.id -ne "deepseek-girl-codex-pet") { throw "Unexpected pet id" }
if ($Manifest.spriteVersionNumber -ne 2) { throw "spriteVersionNumber must be 2" }
if ($Manifest.spritesheetPath -ne "spritesheet.webp") { throw "Unexpected spritesheetPath" }

$Expected = ((Get-Content -LiteralPath $ChecksumPath -Encoding ASCII) -split "\s+")[0].ToLowerInvariant()
$Actual = (Get-FileHash -LiteralPath $AtlasPath -Algorithm SHA256).Hash.ToLowerInvariant()
if ($Actual -ne $Expected) { throw "spritesheet.webp SHA-256 mismatch" }

$Bytes = [System.IO.File]::ReadAllBytes($AtlasPath)
$Ascii = [System.Text.Encoding]::ASCII.GetString($Bytes)
if (-not $Ascii.Contains("WEBP")) { throw "spritesheet.webp is not a WebP file" }

$Vp8lOffset = -1
for ($Index = 12; $Index -le $Bytes.Length - 13; $Index++) {
    if ($Bytes[$Index] -eq 0x56 -and $Bytes[$Index + 1] -eq 0x50 -and
        $Bytes[$Index + 2] -eq 0x38 -and $Bytes[$Index + 3] -eq 0x4C) {
        $Vp8lOffset = $Index
        break
    }
}
if ($Vp8lOffset -lt 0) { throw "Expected a lossless VP8L WebP atlas" }
if ($Bytes[$Vp8lOffset + 8] -ne 0x2F) { throw "Invalid VP8L signature" }

$Bits = [uint32]$Bytes[$Vp8lOffset + 9] -bor
        ([uint32]$Bytes[$Vp8lOffset + 10] -shl 8) -bor
        ([uint32]$Bytes[$Vp8lOffset + 11] -shl 16) -bor
        ([uint32]$Bytes[$Vp8lOffset + 12] -shl 24)
$Width = 1 + ($Bits -band 0x3FFF)
$Height = 1 + (($Bits -shr 14) -band 0x3FFF)
if ($Width -ne 1536 -or $Height -ne 2288) {
    throw "Unexpected atlas dimensions: ${Width}x${Height}"
}

Write-Host "PASS: manifest, SHA-256, WebP format, and 1536x2288 dimensions are valid."
Write-Host "Atlas SHA-256: $Actual"

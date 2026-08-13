$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$SourceDir = Join-Path $RepoRoot "pet"
$DestinationDir = Join-Path $env:USERPROFILE ".codex\pets\deepseek-girl-codex-pet"

if (-not (Test-Path -LiteralPath (Join-Path $SourceDir "pet.json"))) {
    throw "Missing pet/pet.json"
}
if (-not (Test-Path -LiteralPath (Join-Path $SourceDir "spritesheet.webp"))) {
    throw "Missing pet/spritesheet.webp"
}

New-Item -ItemType Directory -Force -Path $DestinationDir | Out-Null

if (Test-Path -LiteralPath (Join-Path $DestinationDir "pet.json")) {
    $BackupDir = "$DestinationDir.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Copy-Item -LiteralPath $DestinationDir -Destination $BackupDir -Recurse
    Write-Host "Backed up the previous installation to $BackupDir"
}

Copy-Item -LiteralPath (Join-Path $SourceDir "pet.json") -Destination $DestinationDir -Force
Copy-Item -LiteralPath (Join-Path $SourceDir "spritesheet.webp") -Destination $DestinationDir -Force

Write-Host "Installed the DeepSeek Girl Codex pet to $DestinationDir"
Write-Host "Restart Codex Desktop, then select the pet in the pet picker."

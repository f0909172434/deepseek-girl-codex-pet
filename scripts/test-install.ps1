$ErrorActionPreference = "Stop"
$TestRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("pet-install-test-" + [guid]::NewGuid())
$Destination = Join-Path $TestRoot "pet"
$BackupRoot = Join-Path $TestRoot "backups"
try {
    & (Join-Path $PSScriptRoot "install.ps1") -DestinationDir $Destination -BackupRoot $BackupRoot
    $Expected = (Get-FileHash (Join-Path $PSScriptRoot "../pet/spritesheet.webp")).Hash
    if ((Get-FileHash (Join-Path $Destination "spritesheet.webp")).Hash -ne $Expected) {
        throw "Installed atlas differs"
    }
    & (Join-Path $PSScriptRoot "install.ps1") -DestinationDir $Destination -BackupRoot $BackupRoot
    $Backups = @(Get-ChildItem -LiteralPath $BackupRoot -Directory | Where-Object Name -Like "pet.backup-*")
    if ($Backups.Count -ne 1) { throw "Expected one previous-installation backup" }
    if ((Get-FileHash (Join-Path $Backups[0].FullName "spritesheet.webp")).Hash -ne $Expected) {
        throw "Backup differs"
    }
    Write-Host "PASS: isolated install, reinstall and backup. Codex itself was not launched."
} finally {
    if (Test-Path -LiteralPath $TestRoot) { Remove-Item -LiteralPath $TestRoot -Recurse -Force }
}

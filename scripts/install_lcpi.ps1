# Script d'installation LCPI-CLI
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Installation de LCPI-CLI..." -ForegroundColor Green

# Ajouter au PATH utilisateur
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$projectPath*") {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$projectPath", "User")
    Write-Host "Chemin ajoute au PATH utilisateur: $projectPath" -ForegroundColor Green
} else {
    Write-Host "Le chemin est deja dans le PATH" -ForegroundColor Blue
}

Write-Host "Installation terminee!" -ForegroundColor Green
Write-Host "Redemarrez votre terminal pour utiliser lcpi depuis n'importe ou." -ForegroundColor Yellow

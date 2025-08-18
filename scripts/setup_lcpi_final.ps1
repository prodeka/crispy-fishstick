# Configuration finale de LCPI-CLI
$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$lcpiPath = Join-Path $projectPath "lcpi.bat"

Write-Host "Configuration finale de LCPI-CLI..." -ForegroundColor Green

# Créer l'alias pour la session actuelle
Set-Alias -Name lcpi -Value $lcpiPath -Scope Global

# Ajouter l'alias au profil PowerShell
$profilePath = $PROFILE.CurrentUserAllHosts
$profileDir = Split-Path $profilePath -Parent

if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

$aliasCommand = "Set-Alias -Name lcpi -Value '$lcpiPath' -Scope Global"

if (Test-Path $profilePath) {
    $content = Get-Content $profilePath
    if ($content -notcontains $aliasCommand) {
        Add-Content $profilePath "`n$aliasCommand"
        Write-Host "Alias ajoute au profil PowerShell" -ForegroundColor Green
    } else {
        Write-Host "L'alias existe deja dans le profil" -ForegroundColor Blue
    }
} else {
    Set-Content $profilePath $aliasCommand
    Write-Host "Profil PowerShell cree avec l'alias" -ForegroundColor Green
}

Write-Host "Configuration terminee!" -ForegroundColor Green
Write-Host "Vous pouvez maintenant utiliser 'lcpi' depuis n'importe ou." -ForegroundColor Yellow

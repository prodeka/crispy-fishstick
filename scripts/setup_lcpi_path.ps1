# Script PowerShell pour configurer LCPI-CLI dans le PATH
# Exécutez ce script en tant qu'administrateur

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$lcpiPath = Join-Path $projectPath "lcpi.bat"

Write-Host "Configuration de LCPI-CLI dans le PATH..." -ForegroundColor Green
Write-Host "Chemin du projet: $projectPath" -ForegroundColor Yellow
Write-Host "Script LCPI: $lcpiPath" -ForegroundColor Yellow

# Vérifier si le script existe
if (-not (Test-Path $lcpiPath)) {
    Write-Host "❌ Erreur: Le script lcpi.bat n'existe pas!" -ForegroundColor Red
    exit 1
}

# Ajouter au PATH utilisateur (pas besoin d'admin)
$userPath = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($userPath -notlike "*$projectPath*") {
    [Environment]::SetEnvironmentVariable("PATH", "$userPath;$projectPath", "User")
    Write-Host "✅ Chemin ajouté au PATH utilisateur" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Le chemin est déjà dans le PATH utilisateur" -ForegroundColor Blue
}

# Créer un alias PowerShell
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
        Write-Host "✅ Alias PowerShell ajouté au profil" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  L'alias PowerShell existe déjà" -ForegroundColor Blue
    }
} else {
    Set-Content $profilePath $aliasCommand
    Write-Host "✅ Profil PowerShell créé avec l'alias" -ForegroundColor Green
}

# Créer l'alias pour la session actuelle
Set-Alias -Name lcpi -Value $lcpiPath -Scope Global

Write-Host "`n🎉 Configuration terminée!" -ForegroundColor Green
Write-Host "Vous pouvez maintenant utiliser 'lcpi' depuis n'importe où." -ForegroundColor Cyan
Write-Host "Exemple: lcpi --help" -ForegroundColor Cyan
Write-Host "`nNote: Redémarrez votre terminal ou exécutez 'refreshenv' pour que les changements prennent effet." -ForegroundColor Yellow

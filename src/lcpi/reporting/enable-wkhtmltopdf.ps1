# reporting/enable-wkhtmltopdf.ps1
param (
    [string]$VendorPath = "..\vendor\wkhtmltopdf\bin"
)

Write-Host "🔧 Configuration wkhtmltopdf..."

# Résout le chemin relatif en absolu
$binPath = Resolve-Path $VendorPath

# Ajoute temporairement au PATH de la session
$env:Path = "$binPath;$env:Path"

# Vérifie si wkhtmltopdf est dispo
try {
    $version = & wkhtmltopdf --version
    Write-Host "✅ wkhtmltopdf prêt : $version"
} catch {
    Write-Host "❌ wkhtmltopdf introuvable dans $binPath"
    exit 1
}

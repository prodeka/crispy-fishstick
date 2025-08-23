# reporting/enable-wkhtmltopdf.ps1
# Usage: .\enable-wkhtmltopdf.ps1  (dot-source pour affecter la session courante) ou exécution simple pour imprimer l'ajout au PATH
param(
  [string]$VendorRelative = "..\vendor\wkhtmltopdf\bin"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vendor = Join-Path $scriptDir $VendorRelative

if (-Not (Test-Path $vendor)) {
  Write-Error "Vendor wkhtmltopdf bin introuvable: $vendor"
  exit 1
}

# Ajouter au PATH du processus courant
$env:PATH = "$vendor;$env:PATH"
Write-Output "wkhtmltopdf bin ajouté au PATH pour la session courante: $vendor"

# Vérification optionnelle
try {
  $out = & wkhtmltopdf --version 2>&1
  Write-Output "wkhtmltopdf present: $out"
} catch {
  Write-Warning "wkhtmltopdf non exécutable depuis PATH. Vérifier permission ou architecture binaire"
}

# reporting/enable-wkhtmltopdf.ps1
param(
	[string]$VendorRelative = "..\vendor\wkhtmltopdf\bin"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$vendor = Join-Path $scriptDir $VendorRelative

if (-Not (Test-Path $vendor)) {
	Write-Error "Vendor wkhtmltopdf bin introuvable: $vendor"
	exit 1
}

$env:PATH = "$vendor;$env:PATH"
Write-Output "wkhtmltopdf bin ajouté au PATH pour la session courante: $vendor"

try {
	$out = & wkhtmltopdf --version 2>&1
	Write-Output "wkhtmltopdf present: $out"
} catch {
	Write-Warning "wkhtmltopdf non exécutable depuis PATH. Vérifier permission ou architecture binaire"
}

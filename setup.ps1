 # =============================================================================
# SCRIPT SETUP AUTOMATICO - Django Starter Project (Windows PowerShell)
# =============================================================================
# Questo script configura automaticamente l'ambiente di sviluppo su Windows

$ErrorActionPreference = "Stop"

Write-Host "Setup Automatico Progetto Django" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Verifica prerequisiti
Write-Host "Verifico prerequisiti..." -ForegroundColor Yellow

# Verifica Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python trovato: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRORE] Python non trovato! Installalo prima di continuare." -ForegroundColor Red
    exit 1
}

# Verifica Node.js
try {
    $nodeVersion = node --version
    Write-Host "[OK] Node.js trovato: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRORE] Node.js non trovato! Installalo prima di continuare." -ForegroundColor Red
    exit 1
}

# Verifica npm
try {
    $npmVersion = npm --version
    Write-Host "[OK] npm trovato: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERRORE] npm non trovato! Installalo prima di continuare." -ForegroundColor Red
    exit 1
}

Write-Host ""

# 1. Virtual Environment Python
Write-Host "[1/6] Creo virtual environment Python..." -ForegroundColor Yellow
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "[OK] Virtual environment creato" -ForegroundColor Green
} else {
    Write-Host "[OK] Virtual environment già esistente" -ForegroundColor Green
}

# 2. Installa Dipendenze Python
Write-Host "[2/6] Installo dipendenze Python..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe -m pip install --upgrade pip -q
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
Write-Host "[OK] Dipendenze Python installate" -ForegroundColor Green

# 3. Installa Dipendenze npm
Write-Host "[3/6] Installo dipendenze npm..." -ForegroundColor Yellow
npm install
Write-Host "[OK] Dipendenze npm installate" -ForegroundColor Green

# 4. Setup Frontend (IMPORTANTE: copia Bootstrap e font in locale)
Write-Host "[4/6] Setup frontend..." -ForegroundColor Yellow

# Copia Bootstrap CSS
Write-Host "  - Copio Bootstrap CSS..."
Copy-Item "node_modules\bootstrap\dist\css\bootstrap.min.css" -Destination "parco_verismo\static\css\" -Force
Write-Host "  [OK] Bootstrap CSS copiato" -ForegroundColor Green

# Copia Bootstrap JS
Write-Host "  - Copio Bootstrap JS..."
if (-not (Test-Path "parco_verismo\static\js")) {
    New-Item -ItemType Directory -Path "parco_verismo\static\js" -Force | Out-Null
}
Copy-Item "node_modules\bootstrap\dist\js\bootstrap.bundle.min.js" -Destination "parco_verismo\static\js\" -Force
Write-Host "  [OK] Bootstrap JS copiato" -ForegroundColor Green

# Copia Font Montserrat
Write-Host "  - Copio font Montserrat..."
if (-not (Test-Path "parco_verismo\static\fonts\montserrat")) {
    New-Item -ItemType Directory -Path "parco_verismo\static\fonts\montserrat" -Force | Out-Null
}
if (Test-Path "node_modules\@fontsource\montserrat\files") {
    Copy-Item "node_modules\@fontsource\montserrat\files\*" -Destination "parco_verismo\static\fonts\montserrat\" -Recurse -Force
}
Write-Host "  [OK] Font Montserrat copiato" -ForegroundColor Green

# Copia Font Inter
Write-Host "  - Copio font Inter..."
if (-not (Test-Path "parco_verismo\static\fonts\inter")) {
    New-Item -ItemType Directory -Path "parco_verismo\static\fonts\inter" -Force | Out-Null
}
if (Test-Path "node_modules\@fontsource\inter\files") {
    Copy-Item "node_modules\@fontsource\inter\files\*" -Destination "parco_verismo\static\fonts\inter\" -Recurse -Force
}
Write-Host "  [OK] Font Inter copiato" -ForegroundColor Green

Write-Host "[OK] Frontend configurato completamente" -ForegroundColor Green

# 5. Setup Database Django
Write-Host "[5/6] Setup database Django..." -ForegroundColor Yellow
& .\.venv\Scripts\python.exe manage.py migrate
Write-Host "[OK] Database configurato" -ForegroundColor Green

# Verifica che Bootstrap sia stato copiato correttamente
Write-Host ""
Write-Host "Verifico installazione Bootstrap..." -ForegroundColor Yellow

if (Test-Path "parco_verismo\static\css\bootstrap.min.css") {
    $size = (Get-Item "parco_verismo\static\css\bootstrap.min.css").Length / 1KB
    Write-Host "[OK] Bootstrap CSS presente ($([math]::Round($size, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "[ERRORE] Bootstrap CSS NON trovato!" -ForegroundColor Red
}

if (Test-Path "parco_verismo\static\js\bootstrap.bundle.min.js") {
    $size = (Get-Item "parco_verismo\static\js\bootstrap.bundle.min.js").Length / 1KB
    Write-Host "[OK] Bootstrap JS presente ($([math]::Round($size, 2)) KB)" -ForegroundColor Green
} else {
    Write-Host "[ERRORE] Bootstrap JS NON trovato!" -ForegroundColor Red
}

if (Test-Path "parco_verismo\static\css\styles.css") {
    Write-Host "[OK] CSS personalizzato presente" -ForegroundColor Green
} else {
    Write-Host "[ERRORE] CSS personalizzato NON trovato!" -ForegroundColor Red
}

# Fine
Write-Host ""
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "SETUP COMPLETATO CON SUCCESSO!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Prossimi passi:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Crea un superuser admin:"
Write-Host "     .\.venv\Scripts\python.exe manage.py createsuperuser"
Write-Host ""
Write-Host "  2. Avvia il server Django:"
Write-Host "     .\.venv\Scripts\python.exe manage.py runserver"
Write-Host ""
Write-Host "  3. Apri il browser su:"
Write-Host "     http://127.0.0.1:8000/"
Write-Host ""
Write-Host "  4. Per l'admin panel:"
Write-Host "     http://127.0.0.1:8000/admin/"
Write-Host ""
Write-Host "Ricorda:" -ForegroundColor Yellow
Write-Host "   - Attiva sempre il virtual environment:"
Write-Host "     .\.venv\Scripts\Activate.ps1    (PowerShell)"
Write-Host "     .venv\Scripts\activate.bat      (CMD)"
Write-Host ""
Write-Host "   - Per modificare stili: edita parco_verismo/static/css/styles.css"
Write-Host ""

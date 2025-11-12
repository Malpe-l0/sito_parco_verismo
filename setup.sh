#!/bin/bash
# =============================================================================
# SCRIPT SETUP AUTOMATICO - Django Starter Project
# =============================================================================
# Questo script configura automaticamente l'ambiente di sviluppo

set -e  # Ferma se c'è un errore

echo "Setup Automatico Progetto Django"
echo "===================================="
echo ""

# Colori per output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verifica prerequisiti
printf "${YELLOW}Verifico prerequisiti...${NC}\n"

# Verifica Python
if ! command -v python3 &> /dev/null; then
    printf "${RED}[ERRORE] Python 3 non trovato! Installalo prima di continuare.${NC}\n"
    exit 1
fi
printf "${GREEN}[OK] Python 3 trovato: $(python3 --version)${NC}\n"

# Verifica Node.js
if ! command -v node &> /dev/null; then
    printf "${RED}[ERRORE] Node.js non trovato! Installalo prima di continuare.${NC}\n"
    exit 1
fi
printf "${GREEN}[OK] Node.js trovato: $(node --version)${NC}\n"

# Verifica npm
if ! command -v npm &> /dev/null; then
    printf "${RED}[ERRORE] npm non trovato! Installalo prima di continuare.${NC}\n"
    exit 1
fi
printf "${GREEN}[OK] npm trovato: $(npm --version)${NC}\n"

echo ""

# 1. Virtual Environment Python
printf "${YELLOW}[1/6] Creo virtual environment Python...${NC}\n"
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    printf "${GREEN}[OK] Virtual environment creato${NC}\n"
else
    printf "${GREEN}[OK] Virtual environment già esistente${NC}\n"
fi

# 2. Attiva Virtual Environment
printf "${YELLOW}[2/6] Attivo virtual environment...${NC}\n"
source .venv/bin/activate
printf "${GREEN}[OK] Virtual environment attivo${NC}\n"

# 3. Installa Dipendenze Python
printf "${YELLOW}[3/6] Installo dipendenze Python...${NC}\n"
pip install --upgrade pip -q
pip install -r requirements.txt
printf "${GREEN}[OK] Dipendenze Python installate${NC}\n"

# 4. Installa Dipendenze npm
printf "${YELLOW}[4/6] Installo dipendenze npm...${NC}\n"
npm install
printf "${GREEN}[OK] Dipendenze npm installate${NC}\n"

# 5. Setup Frontend (IMPORTANTE: copia Bootstrap e font in locale)
printf "${YELLOW}[5/6] Setup frontend...${NC}\n"

# Copia Bootstrap CSS
echo "  - Copio Bootstrap CSS..."
cp node_modules/bootstrap/dist/css/bootstrap.min.css parco_verismo/static/css/
printf "${GREEN}  [OK] Bootstrap CSS copiato${NC}\n"

# Copia Bootstrap JS
echo "  - Copio Bootstrap JS..."
mkdir -p parco_verismo/static/js
cp node_modules/bootstrap/dist/js/bootstrap.bundle.min.js parco_verismo/static/js/
printf "${GREEN}  [OK] Bootstrap JS copiato${NC}\n"

# Copia Font Montserrat
echo "  - Copio font Montserrat..."
mkdir -p parco_verismo/static/fonts/montserrat
cp -r node_modules/@fontsource/montserrat/files/* parco_verismo/static/fonts/montserrat/ 2>/dev/null || true
printf "${GREEN}  [OK] Font Montserrat copiato${NC}\n"

# Copia Font Inter
echo "  - Copio font Inter..."
mkdir -p parco_verismo/static/fonts/inter
cp -r node_modules/@fontsource/inter/files/* parco_verismo/static/fonts/inter/ 2>/dev/null || true
printf "${GREEN}  [OK] Font Inter copiato${NC}\n"

printf "${GREEN}[OK] Frontend configurato completamente${NC}\n"

# 6. Setup Database Django
printf "${YELLOW}[6/6] Setup database Django...${NC}\n"
python manage.py migrate
printf "${GREEN}[OK] Database configurato${NC}\n"

# Verifica che Bootstrap sia stato copiato correttamente
echo ""
printf "${YELLOW}Verifico installazione Bootstrap...${NC}\n"
if [ -f "parco_verismo/static/css/bootstrap.min.css" ]; then
    SIZE=$(du -h parco_verismo/static/css/bootstrap.min.css | cut -f1)
    printf "${GREEN}[OK] Bootstrap CSS presente (${SIZE})${NC}\n"
else
    printf "${RED}[ERRORE] Bootstrap CSS NON trovato!${NC}\n"
fi

if [ -f "parco_verismo/static/js/bootstrap.bundle.min.js" ]; then
    SIZE=$(du -h parco_verismo/static/js/bootstrap.bundle.min.js | cut -f1)
    printf "${GREEN}[OK] Bootstrap JS presente (${SIZE})${NC}\n"
else
    printf "${RED}[ERRORE] Bootstrap JS NON trovato!${NC}\n"
fi

if [ -f "parco_verismo/static/css/styles.css" ]; then
    printf "${GREEN}[OK] CSS personalizzato presente${NC}\n"
else
    printf "${RED}[ERRORE] CSS personalizzato NON trovato!${NC}\n"
fi

# Fine
echo ""
echo "===================================="
printf "${GREEN}SETUP COMPLETATO CON SUCCESSO!${NC}\n"
echo "===================================="
echo ""
printf "${YELLOW}Prossimi passi:${NC}\n"
echo ""
echo "  1. Crea un superuser admin:"
echo "     python manage.py createsuperuser"
echo ""
echo "  2. Avvia il server Django:"
echo "     python manage.py runserver"
echo ""
echo "  3. Apri il browser su:"
echo "     http://127.0.0.1:8000/"
echo ""
echo "  4. Per l'admin panel:"
echo "     http://127.0.0.1:8000/admin/"
echo ""
printf "${YELLOW}Ricorda:${NC}\n"
echo "   - Attiva sempre il virtual environment:"
echo "     source .venv/bin/activate   (Linux/Mac)"
echo "     .venv\\Scripts\\activate      (Windows)"
echo ""
echo "   - Per modificare stili: edita parco_verismo/static/css/styles.css"
echo ""

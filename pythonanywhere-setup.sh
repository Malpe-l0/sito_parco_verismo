#!/usr/bin/env bash
# =============================================================================
# PYTHONANYWHERE SETUP - Script di configurazione per PythonAnywhere
# =============================================================================
# Da eseguire nella console Bash di PythonAnywhere dopo aver caricato i file
#
# Uso: bash pythonanywhere-setup.sh
#
# PREREQUISITI:
# 1. Aver creato account PythonAnywhere
# 2. Aver caricato i file del progetto
# 3. Essere nella directory del progetto
# =============================================================================

set -euo pipefail

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
printf "${CYAN}╔═══════════════════════════════════════════════╗${NC}\n"
printf "${CYAN}║  PYTHONANYWHERE SETUP - Parco Verismo        ║${NC}\n"
printf "${CYAN}╚═══════════════════════════════════════════════╝${NC}\n"
echo ""

# Verifica di essere su PythonAnywhere
if [ ! -d "/home/$USER" ]; then
    printf "${RED}❌ Questo script è pensato per PythonAnywhere${NC}\n"
    exit 1
fi

VENV_DIR="venv"
PROJECT_DIR="$PWD"

# 1. Virtual Environment
printf "${YELLOW}[1/6]${NC} Creazione virtual environment...\n"
if [ ! -d "$VENV_DIR" ]; then
    python3.10 -m venv "$VENV_DIR"
    printf "${GREEN}✓${NC} Virtual environment creato\n\n"
else
    printf "${GREEN}✓${NC} Virtual environment già esistente\n\n"
fi

# Attiva virtualenv
source "$VENV_DIR/bin/activate"

# 2. Installazione dipendenze
printf "${YELLOW}[2/6]${NC} Installazione dipendenze Python...\n"
pip install --upgrade pip
pip install -r requirements.txt
printf "${GREEN}✓${NC} Dipendenze installate\n\n"

# 3. Configurazione .env
printf "${YELLOW}[3/6]${NC} Configurazione file .env...\n"
if [ ! -f .env ]; then
    if [ -f .env.pythonanywhere ]; then
        cp .env.pythonanywhere .env
        
        # Genera SECRET_KEY casuale
        SECRET_KEY=$(python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
        sed -i "s/SECRET_KEY=.*/SECRET_KEY=$SECRET_KEY/" .env
        
        # Sostituisci username
        sed -i "s/your_username/$USER/g" .env
        
        printf "${GREEN}✓${NC} File .env creato\n"
        printf "${YELLOW}⚠${NC}  IMPORTANTE: Modifica .env e aggiungi il tuo dominio in ALLOWED_HOSTS\n"
        printf "   Es: ALLOWED_HOSTS=$USER.pythonanywhere.com\n\n"
    else
        printf "${RED}❌ File .env.pythonanywhere non trovato!${NC}\n"
        exit 1
    fi
else
    printf "${GREEN}✓${NC} File .env già esistente\n\n"
fi

# 4. Migrazioni database
printf "${YELLOW}[4/6]${NC} Esecuzione migrazioni database...\n"
python manage.py migrate
printf "${GREEN}✓${NC} Migrazioni completate\n\n"

# 5. Raccolta file statici
printf "${YELLOW}[5/6]${NC} Raccolta file statici...\n"
python manage.py collectstatic --noinput
printf "${GREEN}✓${NC} File statici raccolti\n\n"

# 6. Creazione superuser
printf "${YELLOW}[6/6]${NC} Creazione superuser...\n"
printf "${CYAN}Inserisci i dati per l'amministratore:${NC}\n"
python manage.py createsuperuser

printf "\n${GREEN}╔═══════════════════════════════════════════════╗${NC}\n"
printf "${GREEN}║          SETUP COMPLETATO CON SUCCESSO!       ║${NC}\n"
printf "${GREEN}╚═══════════════════════════════════════════════╝${NC}\n\n"

printf "${CYAN}PROSSIMI PASSI:${NC}\n"
printf "1. Modifica ${YELLOW}.env${NC} con il tuo dominio in ALLOWED_HOSTS\n"
printf "2. Vai su Web → Add a new web app\n"
printf "3. Scegli 'Manual configuration' → Python 3.10\n"
printf "4. Configura il WSGI file (vedi DEPLOY_PYTHONANYWHERE.md)\n"
printf "5. Configura Static files:\n"
printf "   URL: ${YELLOW}/static/${NC}  Directory: ${YELLOW}$PROJECT_DIR/staticfiles${NC}\n"
printf "   URL: ${YELLOW}/media/${NC}   Directory: ${YELLOW}$PROJECT_DIR/media${NC}\n"
printf "6. Reload dell'app web\n\n"

printf "${CYAN}Per popolare il database con dati demo:${NC}\n"
printf "   source venv/bin/activate\n"
printf "   python populate_db_complete.py\n\n"

printf "${GREEN}✓ Tutto pronto!${NC}\n\n"

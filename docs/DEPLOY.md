# 🚀 Guida Completa al Deployment su VPS Aruba Cloud

Questa guida ti accompagna **passo-passo** nel deployment del Parco Letterario del Verismo su una VPS Aruba Cloud. Segui ogni passaggio nell'ordine indicato.

---

## 📋 Indice

1. [Prerequisiti](#1️⃣-prerequisiti)
2. [Acquisto e Accesso VPS](#2️⃣-acquisto-e-accesso-vps)
3. [Setup Iniziale VPS](#3️⃣-setup-iniziale-vps)
4. [Installazione Docker](#4️⃣-installazione-docker)
5. [Configurazione Firewall](#5️⃣-configurazione-firewall)
6. [Clone del Progetto](#6️⃣-clone-del-progetto)
7. [Configurazione Ambiente](#7️⃣-configurazione-ambiente)
8. [Primo Avvio (HTTP)](#8️⃣-primo-avvio-http)
9. [Configurazione DNS](#9️⃣-configurazione-dns)
10. [Configurazione SSL/HTTPS](#🔟-configurazione-sslhttps)
11. [Creazione Superuser](#1️⃣1️⃣-creazione-superuser)
12. [Backup Automatici](#1️⃣2️⃣-backup-automatici)
13. [GitHub Actions CI/CD](#1️⃣3️⃣-github-actions-cicd)
14. [Comandi Utili](#📊-comandi-utili)
15. [Troubleshooting](#❓-troubleshooting)

---

## 1️⃣ Prerequisiti

Prima di iniziare, assicurati di avere:

| Requisito | Descrizione |
|-----------|-------------|
| **VPS Aruba Cloud** | Piano base sufficiente (1 vCPU, 2GB RAM, 20GB SSD) |
| **Sistema Operativo** | Ubuntu 22.04 LTS (selezionalo durante l'acquisto) |
| **Dominio** | Un dominio già acquistato (es. parcoverismo.it) |
| **Client SSH** | Terminale Mac/Linux o PuTTY su Windows |
| **Account GitHub** | Per il repository del progetto |

---

## 2️⃣ Acquisto e Accesso VPS

### 2.1 Acquista la VPS su Aruba Cloud

1. Vai su [cloud.aruba.it](https://cloud.aruba.it)
2. Seleziona **Cloud VPS** → **Acquista**
3. Scegli il piano (consigliato: **VPS Small** o superiore)
4. **Sistema Operativo**: Seleziona **Ubuntu 22.04 LTS**
5. Completa l'acquisto

### 2.2 Trova l'IP e le Credenziali

Dopo l'acquisto, riceverai un'email con:
- **Indirizzo IP** della VPS (es. `94.177.XXX.XXX`)
- **Password root** temporanea

Puoi trovare queste info anche nel pannello Aruba Cloud → **I tuoi servizi** → **VPS**.

### 2.3 Prima Connessione SSH

Apri il terminale e connettiti:

```bash
ssh root@TUO_IP_VPS
```

**Esempio:**
```bash
ssh root@94.177.123.45
```

Ti chiederà:
1. `Are you sure you want to continue connecting?` → Scrivi `yes` e premi Invio
2. Inserisci la password ricevuta via email

> ⚠️ **IMPORTANTE**: Al primo accesso potrebbe chiederti di cambiare la password. Scegli una password sicura e **salvala in un posto sicuro!**

---

## 3️⃣ Setup Iniziale VPS

### 3.1 Aggiorna il Sistema

Una volta connesso come root, aggiorna tutti i pacchetti:

```bash
apt update && apt upgrade -y
```

Questo può richiedere alcuni minuti. Se chiede conferme, premi `Y` e Invio.

### 3.2 Crea un Utente Non-Root

**Mai usare root per le operazioni quotidiane!** Crea un utente dedicato:

```bash
adduser deploy
```

Ti chiederà:
1. **Password**: Scegli una password sicura (diversa da root)
2. **Full Name**: Puoi lasciare vuoto (premi Invio)
3. **Room Number, Phone, etc.**: Lascia vuoto (premi Invio per ogni campo)
4. **Is the information correct?** → `Y`

### 3.3 Dai Permessi Sudo all'Utente

```bash
usermod -aG sudo deploy
```

### 3.4 Configura Accesso SSH per l'Utente Deploy

```bash
# Crea la directory SSH per deploy
mkdir -p /home/deploy/.ssh

# Copia le chiavi autorizzate
cp ~/.ssh/authorized_keys /home/deploy/.ssh/ 2>/dev/null || touch /home/deploy/.ssh/authorized_keys

# Imposta i permessi corretti
chown -R deploy:deploy /home/deploy/.ssh
chmod 700 /home/deploy/.ssh
chmod 600 /home/deploy/.ssh/authorized_keys
```

### 3.5 (Opzionale ma Consigliato) Configura Chiave SSH dal tuo PC

Sul **tuo computer locale** (non sulla VPS), genera una chiave SSH se non ne hai già una:

```bash
# Sul tuo Mac/Linux locale
ssh-keygen -t ed25519 -C "tua@email.com"
```

Premi Invio per accettare il percorso default. Puoi impostare una passphrase o lasciare vuoto.

Copia la chiave pubblica sulla VPS:

```bash
# Sul tuo Mac/Linux locale
ssh-copy-id deploy@TUO_IP_VPS
```

### 3.6 Verifica Accesso con Utente Deploy

Disconnettiti dalla VPS:

```bash
exit
```

Riconnettiti come utente **deploy**:

```bash
ssh deploy@TUO_IP_VPS
```

Se funziona, sei pronto per il prossimo step!

---

## 4️⃣ Installazione Docker

### 4.1 Installa le Dipendenze

```bash
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
```

### 4.2 Aggiungi il Repository Docker

```bash
# Scarica la chiave GPG di Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Aggiungi il repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

### 4.3 Installa Docker

```bash
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 4.4 Aggiungi l'Utente al Gruppo Docker

Questo permette di usare Docker senza `sudo`:

```bash
sudo usermod -aG docker deploy
```

### 4.5 Applica le Modifiche al Gruppo

```bash
newgrp docker
```

### 4.6 Verifica l'Installazione

```bash
docker --version
docker compose version
```

Dovresti vedere qualcosa tipo:
```
Docker version 24.0.x, build xxxxx
Docker Compose version v2.x.x
```

### 4.7 Test Docker

```bash
docker run hello-world
```

Se vedi "Hello from Docker!", l'installazione è riuscita! 🎉

---

## 5️⃣ Configurazione Firewall

### 5.1 Abilita UFW Firewall

```bash
# Permetti SSH (IMPORTANTE: fallo prima di abilitare il firewall!)
sudo ufw allow OpenSSH

# Permetti HTTP
sudo ufw allow 80/tcp

# Permetti HTTPS
sudo ufw allow 443/tcp

# Abilita il firewall
sudo ufw enable
```

Ti chiederà conferma → `y`

### 5.2 Verifica lo Stato

```bash
sudo ufw status
```

Dovresti vedere:
```
Status: active

To                         Action      From
--                         ------      ----
OpenSSH                    ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

---

## 6️⃣ Clone del Progetto

### 6.1 Posizionati nella Home

```bash
cd ~
```

### 6.2 Clona il Repository

```bash
git clone https://github.com/Triba14/sito_parco_verismo.git
```

### 6.3 Entra nella Directory

```bash
cd sito_parco_verismo
```

### 6.4 Verifica i File

```bash
ls -la
```

Dovresti vedere tutti i file del progetto.

---

## 7️⃣ Configurazione Ambiente

### 7.1 Crea il File di Configurazione Produzione

```bash
cp .env.production .env.production.backup
nano .env.production
```

### 7.2 Modifica le Variabili

Nel file `.env.production`, modifica queste righe:

```bash
# GENERA UNA NUOVA SECRET KEY (vedi sotto come fare)
SECRET_KEY=incolla-qui-la-secret-key-generata

# IMPORTANTE: Imposta a False
DEBUG=False

# IL TUO DOMINIO (senza http://)
ALLOWED_HOSTS=tuodominio.com,www.tuodominio.com

# Lascia False per ora, attiveremo dopo aver configurato SSL
SECURE_SSL_REDIRECT=False
```

**Come generare SECRET_KEY:**

Apri un altro terminale sulla VPS o usa questo comando:

```bash
python3 -c 'import secrets; print(secrets.token_urlsafe(50))'
```

Copia l'output e incollalo come valore di `SECRET_KEY`.

**Salva il file**: `Ctrl+X`, poi `Y`, poi `Invio`

### 7.3 Configura Nginx con il Tuo Dominio

```bash
nano nginx/conf.d/default.conf
```

**Trova e sostituisci** tutte le occorrenze di `YOUR_DOMAIN.com` con il tuo dominio reale.

**Tip**: In nano, premi `Ctrl+\` per cercare e sostituire:
1. Cerca: `YOUR_DOMAIN.com`
2. Sostituisci con: `tuodominio.com`
3. Premi `A` per sostituire tutte le occorrenze

**Salva**: `Ctrl+X`, `Y`, `Invio`

### 7.4 Configura lo Script SSL

```bash
nano scripts/ssl-setup.sh
```

Modifica queste due righe all'inizio:

```bash
DOMAIN="tuodominio.com"
EMAIL="tua@email.com"
```

**Salva**: `Ctrl+X`, `Y`, `Invio`

---

## 8️⃣ Primo Avvio (HTTP)

### 8.1 Costruisci e Avvia i Container

```bash
docker compose up -d --build
```

Questo comando:
1. Costruisce l'immagine Docker del progetto
2. Scarica le immagini di Nginx e Certbot
3. Avvia tutti i servizi

**La prima volta può richiedere 3-5 minuti.**

### 8.2 Verifica che Tutto Funzioni

```bash
docker compose ps
```

Dovresti vedere qualcosa tipo:
```
NAME                    STATUS
parco_verismo_web       Up
parco_verismo_nginx     Up
parco_verismo_init      Exited (0)
```

> `init` mostra "Exited" perché è un container che esegue le migrazioni e poi termina. È normale!

### 8.3 Controlla i Log

```bash
docker compose logs -f
```

Premi `Ctrl+C` per uscire dai log.

Se vedi errori, controlla la sezione [Troubleshooting](#❓-troubleshooting).

### 8.4 Test Locale

```bash
curl http://localhost
```

Dovresti vedere l'HTML della homepage.

---

## 9️⃣ Configurazione DNS

### 9.1 Accedi al Pannello del Tuo Registrar

Vai sul sito dove hai acquistato il dominio (es. Aruba, GoDaddy, Cloudflare, etc.)

### 9.2 Configura i Record DNS

Aggiungi o modifica questi record:

| Tipo | Nome | Valore | TTL |
|------|------|--------|-----|
| A | @ | TUO_IP_VPS | 300 |
| A | www | TUO_IP_VPS | 300 |

**Esempio:**
- Tipo: `A`
- Nome: `@` (o lascia vuoto per il dominio principale)
- Valore: `94.177.123.45` (il tuo IP VPS)
- TTL: `300` (o "5 minuti")

### 9.3 Attendi la Propagazione DNS

La propagazione DNS può richiedere da 5 minuti a 48 ore, ma di solito è veloce.

**Verifica la propagazione:**

```bash
# Sulla VPS
dig +short tuodominio.com
```

Quando vedi il tuo IP, il DNS è propagato!

**Oppure usa un servizio online:** [whatsmydns.net](https://www.whatsmydns.net)

### 9.4 Testa l'Accesso via Browser

Apri nel browser: `http://tuodominio.com`

Dovresti vedere il sito! (senza HTTPS per ora)

---

## 🔟 Configurazione SSL/HTTPS

> ⚠️ **IMPORTANTE**: Esegui questo step SOLO dopo che il DNS è propagato e il sito è accessibile via HTTP!

### 10.1 Esegui lo Script SSL

```bash
chmod +x scripts/ssl-setup.sh
./scripts/ssl-setup.sh
```

Lo script:
1. Richiede un certificato SSL a Let's Encrypt
2. Configura il rinnovo automatico

### 10.2 Attiva HTTPS nella Configurazione Nginx

```bash
nano nginx/conf.d/default.conf
```

**Fai queste modifiche:**

#### A) Attiva il redirect HTTP → HTTPS (righe ~31-33)

PRIMA (commentato):
```nginx
    # location / {
    #     return 301 https://$host$request_uri;
    # }
```

DOPO (decommentato):
```nginx
    location / {
        return 301 https://$host$request_uri;
    }
```

#### B) Commenta la sezione HTTP location (righe ~35-47)

PRIMA:
```nginx
    location / {
        proxy_pass http://django_app;
        ...
    }
```

DOPO (aggiungi # all'inizio di ogni riga):
```nginx
    # location / {
    #     proxy_pass http://django_app;
    #     ...
    # }
```

#### C) Decommenta TUTTO il blocco HTTPS (righe ~75-125)

Rimuovi il `#` all'inizio di ogni riga del blocco HTTPS.

PRIMA:
```nginx
# server {
#     listen 443 ssl http2;
#     ...
# }
```

DOPO:
```nginx
server {
    listen 443 ssl http2;
    ...
}
```

**Salva**: `Ctrl+X`, `Y`, `Invio`

### 10.3 Riavvia Nginx

```bash
docker compose restart nginx
```

### 10.4 Attiva SECURE_SSL_REDIRECT in Django

```bash
nano .env.production
```

Cambia:
```bash
SECURE_SSL_REDIRECT=True
```

**Salva** e riavvia Django:

```bash
docker compose restart web
```

### 10.5 Verifica HTTPS

Apri nel browser: `https://tuodominio.com`

Dovresti vedere:
- 🔒 Il lucchetto verde nella barra degli indirizzi
- Il sito caricato correttamente

**Test redirect HTTP:**
Apri `http://tuodominio.com` - dovrebbe reindirizzare automaticamente a HTTPS.

---

## 1️⃣1️⃣ Creazione Superuser

### 11.1 Crea l'Account Admin

```bash
docker compose exec web python manage.py createsuperuser
```

Ti chiederà:
1. **Username**: scegli un nome (es. `admin`)
2. **Email**: la tua email
3. **Password**: una password sicura (almeno 8 caratteri)

### 11.2 Accedi al Pannello Admin

Vai su: `https://tuodominio.com/admin/`

Inserisci le credenziali appena create.

---

## 1️⃣2️⃣ Backup Automatici

### 12.1 Crea la Directory Backup

```bash
mkdir -p ~/backups
```

### 12.2 Rendi Eseguibile lo Script

```bash
chmod +x scripts/backup.sh
```

### 12.3 Testa il Backup

```bash
./scripts/backup.sh
```

Dovresti vedere un output tipo:
```
[data] Inizio backup...
Backup database SQLite...
✓ Database: 52K
Backup media files...
✓ Media: 1.2M
========================================
   BACKUP COMPLETATO
========================================
```

### 12.4 Configura Backup Automatico (Cron)

```bash
crontab -e
```

Se chiede quale editor usare, scegli `nano` (opzione 1).

Aggiungi questa riga alla fine del file:

```
0 2 * * * /home/deploy/sito_parco_verismo/scripts/backup.sh >> /home/deploy/backups/backup.log 2>&1
```

Questo esegue il backup ogni giorno alle 2:00 di notte.

**Salva**: `Ctrl+X`, `Y`, `Invio`

### 12.5 Verifica il Cron

```bash
crontab -l
```

Dovresti vedere la riga che hai aggiunto.

---

## 1️⃣3️⃣ GitHub Actions CI/CD

### 13.1 Genera Chiave SSH per GitHub Actions

Sulla VPS, genera una nuova chiave SSH dedicata:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_actions -N ""
```

### 13.2 Aggiungi la Chiave Pubblica alle Authorized Keys

```bash
cat ~/.ssh/github_actions.pub >> ~/.ssh/authorized_keys
```

### 13.3 Visualizza la Chiave Privata

```bash
cat ~/.ssh/github_actions
```

**Copia tutto l'output**, incluse le righe `-----BEGIN` e `-----END`.

### 13.4 Configura i Secrets su GitHub

1. Vai su GitHub → Il tuo repository → **Settings**
2. Nel menu laterale: **Secrets and variables** → **Actions**
3. Clicca **New repository secret**

Aggiungi questi 4 secrets (uno alla volta):

| Nome Secret | Valore |
|-------------|--------|
| `VPS_HOST` | L'IP della tua VPS (es. `94.177.123.45`) |
| `VPS_USER` | `deploy` |
| `VPS_SSH_KEY` | Incolla tutta la chiave privata copiata prima |
| `VPS_PATH` | `/home/deploy/sito_parco_verismo` |

### 13.5 Testa il Deploy Automatico

Sul tuo computer locale, fai un commit e push:

```bash
git add .
git commit -m "Test deploy automatico"
git push origin main
```

### 13.6 Monitora il Deploy

1. Vai su GitHub → Il tuo repository → **Actions**
2. Clicca sul workflow in esecuzione
3. Osserva i log per verificare che tutto vada a buon fine

Se vedi ✅ verde, il deploy è riuscito!

---

## 📊 Comandi Utili

### Gestione Container

```bash
# Stato di tutti i servizi
docker compose ps

# Log in tempo reale (tutti i servizi)
docker compose logs -f

# Log di un singolo servizio
docker compose logs -f web
docker compose logs -f nginx

# Riavvia tutti i servizi
docker compose restart

# Riavvia un singolo servizio
docker compose restart web
docker compose restart nginx

# Ferma tutti i servizi
docker compose down

# Ricostruisci e riavvia (dopo modifiche al codice)
docker compose up -d --build

# Rimuovi container, volumi e immagini inutilizzate
docker system prune -a
```

### Django

```bash
# Shell interattiva Django
docker compose exec web python manage.py shell

# Esegui migrazioni
docker compose exec web python manage.py migrate

# Crea nuove migrazioni
docker compose exec web python manage.py makemigrations

# Raccogli file statici
docker compose exec web python manage.py collectstatic --noinput

# Crea superuser
docker compose exec web python manage.py createsuperuser

# Verifica configurazione
docker compose exec web python manage.py check --deploy
```

### Backup

```bash
# Backup manuale
./scripts/backup.sh

# Visualizza backup esistenti
ls -lh ~/backups/

# Ripristina database da backup
gunzip -k ~/backups/db_XXXXXX.sqlite3.gz
docker cp ~/backups/db_XXXXXX.sqlite3 parco_verismo_web:/app/db.sqlite3
docker compose restart web
```

### Aggiornamenti

```bash
# Aggiornamento manuale
cd ~/sito_parco_verismo
git pull origin main
docker compose up -d --build

# Aggiorna sistema operativo VPS
sudo apt update && sudo apt upgrade -y

# Aggiorna Docker
sudo apt update && sudo apt install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### SSL

```bash
# Stato certificato
docker compose exec nginx ls -la /etc/letsencrypt/live/

# Rinnova certificato manualmente
docker compose run --rm certbot renew
docker compose restart nginx

# Verifica scadenza certificato
docker compose run --rm certbot certificates
```

---

## ❓ Troubleshooting

### ❌ Il sito non si carica

**Verifica i container:**
```bash
docker compose ps
```

Tutti devono mostrare `Up`. Se qualcuno è `Exited` con errore:
```bash
docker compose logs nome_servizio
```

**Verifica firewall:**
```bash
sudo ufw status
```

Le porte 80 e 443 devono essere aperte.

**Verifica DNS:**
```bash
dig +short tuodominio.com
```

Deve mostrare l'IP della VPS.

---

### ❌ Errore 502 Bad Gateway

Il container web non risponde. Verifica:

```bash
docker compose logs web
```

**Possibili cause:**
- Errore nelle migrazioni
- Variabili ambiente non configurate
- Errore nel codice Python

**Soluzione:**
```bash
docker compose down
docker compose up -d --build
docker compose logs -f web
```

---

### ❌ Static files non caricati (stili mancanti)

```bash
docker compose exec web python manage.py collectstatic --noinput
docker compose restart nginx
```

---

### ❌ HTTPS non funziona

**Verifica certificato:**
```bash
docker compose exec nginx ls -la /etc/letsencrypt/live/
```

Se la directory è vuota, riesegui lo script SSL:
```bash
./scripts/ssl-setup.sh
```

**Verifica configurazione Nginx:**
```bash
docker compose exec nginx nginx -t
```

Deve mostrare `syntax is ok`.

---

### ❌ Permesso negato con Docker

```bash
sudo usermod -aG docker $USER
newgrp docker
```

Oppure disconnettiti e riconnettiti via SSH.

---

### ❌ Spazio disco esaurito

```bash
# Verifica spazio
df -h

# Pulisci Docker
docker system prune -a

# Pulisci vecchi backup
find ~/backups -mtime +30 -delete
```

---

### ❌ Container non si avvia dopo reboot VPS

Docker dovrebbe riavviarsi automaticamente. Se non succede:

```bash
sudo systemctl enable docker
sudo systemctl start docker
cd ~/sito_parco_verismo
docker compose up -d
```

---

## 📁 Struttura File Deployment

```
sito_parco_verismo/
│
├── .env.production          # ⚙️ Variabili ambiente (SECRET_KEY, ALLOWED_HOSTS)
│
├── .github/
│   └── workflows/
│       └── deploy.yml       # 🚀 GitHub Actions CI/CD
│
├── docker-compose.yml       # 🐳 Orchestrazione container
├── Dockerfile               # 🐳 Build image Django
│
├── nginx/
│   ├── nginx.conf           # 🌐 Config principale
│   └── conf.d/
│       └── default.conf     # 🌐 Server block + SSL
│
├── scripts/
│   ├── ssl-setup.sh         # 🔐 Setup Let's Encrypt
│   └── backup.sh            # 💾 Backup automatico
│
└── docs/
    └── DEPLOY.md            # 📖 Questa guida
```

---

## 🎉 Congratulazioni!

Se sei arrivato fin qui, il tuo sito è online, sicuro con HTTPS, con backup automatici e deploy automatico da GitHub!

**Prossimi passi consigliati:**

1. ✅ Verifica regolarmente i log: `docker compose logs -f`
2. ✅ Monitora i backup: `ls -lh ~/backups/`
3. ✅ Tieni aggiornato il sistema: `sudo apt update && sudo apt upgrade`
4. ✅ Configura Google Analytics nel `.env.production`

---

*Guida creata per Parco Letterario del Verismo - Dicembre 2024*

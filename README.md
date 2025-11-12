# Django Starter Project

Progetto Django base pronto all'uso con Bootstrap 5.

## 🚀 Quick Start

### Setup Automatico

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```powershell
.\setup.ps1
```

### Setup Manuale

```bash
# Crea ambiente virtuale
python3 -m venv .venv
source .venv/bin/activate

# Installa dipendenze
pip install -r requirements.txt
npm install
npm run setup

# Database
python manage.py migrate
python manage.py createsuperuser

# Avvia server
python manage.py runserver
```

**URL**: http://127.0.0.1:8000/
**Admin**: http://127.0.0.1:8000/admin/

## 📦 Stack

- Django 4.2.16, Python 3.8+
- Bootstrap 5.3.3
- SQLite (PostgreSQL ready)

## 🛠️ Sviluppo

### Modello
```python
# parco_verismo/models.py
class MioModello(models.Model):
    titolo = models.CharField(max_length=200)
    contenuto = models.TextField()
```

```bash
python manage.py makemigrations
python manage.py migrate
```

### View
```python
# parco_verismo/views.py
class MiaView(ListView):
    model = MioModello
    template_name = 'parco_verismo/pagina.html'
```

### URL
```python
# parco_verismo/urls.py
path('pagina/', views.MiaView.as_view(), name='pagina'),
```

### Stili
Modifica `parco_verismo/static/css/styles.css`

## 📝 Comandi

```bash
python manage.py check          # Verifica
python manage.py shell          # Shell
python manage.py test           # Test
python manage.py collectstatic  # Static (produzione)
```

## 📄 Licenza

MIT License

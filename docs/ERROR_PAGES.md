# Pagine di Errore Personalizzate

Questo progetto include pagine di errore personalizzate per migliorare l'esperienza utente quando si verificano errori HTTP.

## Pagine Disponibili

### 404 - Pagina Non Trovata
- **Template**: `templates/404.html`
- **Handler**: `parco_verismo.views.errors.custom_404`
- **Quando**: L'URL richiesto non esiste
- **Features**:
  - Design coerente con il resto del sito
  - Pulsanti per tornare alla home o esplorare la biblioteca
  - Barra di ricerca integrata
  - Animazioni CSS

### 500 - Errore del Server
- **Template**: `templates/500.html`
- **Handler**: `parco_verismo.views.errors.custom_500`
- **Quando**: Si verifica un errore interno del server
- **Features**:
  - Design standalone (non usa base.html per evitare errori ricorsivi)
  - Informazioni di contatto
  - Pulsante per ricaricare la pagina

### 403 - Accesso Negato
- **Template**: `templates/403.html`
- **Handler**: `parco_verismo.views.errors.custom_403`
- **Quando**: L'utente non ha permessi per accedere a una risorsa
- **Features**:
  - Link per effettuare il login (se non autenticato)
  - Pulsante per tornare indietro

### 400 - Richiesta Non Valida
- **Template**: `templates/400.html`
- **Handler**: `parco_verismo.views.errors.custom_400`
- **Quando**: La richiesta contiene dati non validi
- **Features**:
  - Link alla pagina contatti
  - Suggerimenti per risolvere il problema

## Configurazione

Gli handler sono configurati in `mysite/urls.py`:

```python
handler404 = 'parco_verismo.views.errors.custom_404'
handler500 = 'parco_verismo.views.errors.custom_500'
handler403 = 'parco_verismo.views.errors.custom_403'
handler400 = 'parco_verismo.views.errors.custom_400'
```

## Testing

### In Sviluppo (DEBUG=True)

Django non usa automaticamente gli error handlers quando `DEBUG=True`. Per testare le pagine:

1. Usa le view di test create appositamente:

```python
# In mysite/urls.py (SOLO PER TEST)
from parco_verismo.views.test_errors import (
    test_404_view, test_500_view, test_403_view, test_400_view
)

urlpatterns += [
    path('test-404/', test_404_view),
    path('test-500/', test_500_view),
    path('test-403/', test_403_view),
    path('test-400/', test_400_view),
]
```

2. Visita:
   - http://127.0.0.1:8000/test-404/
   - http://127.0.0.1:8000/test-500/
   - http://127.0.0.1:8000/test-403/
   - http://127.0.0.1:8000/test-400/

### In Produzione (DEBUG=False)

In produzione, Django userà automaticamente gli handler personalizzati:

- Visita un URL inesistente per vedere la pagina 404
- Gli errori 500 appariranno automaticamente in caso di errori del server

## Design

Le pagine di errore seguono questi principi:

1. **Coerenza**: Utilizzano lo stesso stile del sito (Bootstrap, colori brand)
2. **Informative**: Spiegano chiaramente cosa è successo
3. **Actionable**: Offrono azioni concrete (torna alla home, cerca, contatta)
4. **Multilingua**: Supportano italiano e inglese via i18n
5. **Responsive**: Funzionano su tutti i dispositivi
6. **Animate**: Piccole animazioni CSS per un'esperienza più piacevole

## Traduzioni

Le stringhe sono tradotte usando il sistema i18n di Django:

```bash
# Aggiorna le traduzioni
python manage.py makemessages -l en
python manage.py makemessages -l it

# Compila le traduzioni
python manage.py compilemessages
```

## Personalizzazione

Per personalizzare le pagine di errore:

1. Modifica i template in `parco_verismo/templates/`
2. Modifica gli handler in `parco_verismo/views/errors.py`
3. Aggiorna gli stili CSS inline o in file esterni

## Note Tecniche

- **404, 403, 400**: Estendono `base.html` per coerenza visiva
- **500**: Template standalone per evitare errori ricorsivi se `base.html` causa problemi
- **Logging**: Gli errori sono automaticamente loggati da Django
- **SEO**: I meta tag sono ottimizzati per evitare indicizzazione delle pagine di errore

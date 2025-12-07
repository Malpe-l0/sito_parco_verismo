from django.db import models
from django.urls import reverse
from parler.models import TranslatableModel, TranslatedFields

class Autore(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    # ... puoi aggiungere biografia, foto, etc.

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Autore"
        verbose_name_plural = "Autori"


class Opera(TranslatableModel):
    autore = models.ForeignKey(Autore, on_delete=models.PROTECT, related_name='opere')
    slug = models.SlugField(max_length=200, unique=True)
    anno_pubblicazione = models.IntegerField(null=True, blank=True)
    link_wikisource = models.URLField(max_length=500, help_text="Link alla pagina dell'opera su Wikisource.")
    copertina = models.ImageField(upload_to="copertine_opere/", blank=True, null=True, help_text="Carica la copertina dell'opera.")

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        trama=models.TextField(help_text="Breve trama o descrizione dell'opera."),
        analisi=models.TextField(blank=True, null=True, help_text="Spunti di analisi o contesto storico."),
    )

    class Meta:
        ordering = ['anno_pubblicazione', 'slug']
        verbose_name = "Opera"
        verbose_name_plural = "Opere"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse('opera_detail', kwargs={'slug': self.slug})


class Evento(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True)
    data_inizio = models.DateTimeField(help_text="Data e ora di inizio dell'evento.")
    data_fine = models.DateTimeField(blank=True, null=True, help_text="Data e ora di fine dell'evento (opzionale).")
    immagine = models.ImageField(upload_to="eventi/", blank=True, null=True, help_text="Immagine rappresentativa dell'evento.")
    is_active = models.BooleanField(default=True, help_text="Se l'evento è attivo e visibile.")

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        descrizione=models.TextField(help_text="Descrizione dettagliata dell'evento."),
        luogo=models.CharField(max_length=200, help_text="Luogo dove si svolge l'evento."),
        indirizzo=models.TextField(blank=True, null=True, help_text="Indirizzo completo del luogo."),
    )

    class Meta:
        ordering = ['-data_inizio']
        verbose_name = "Evento"
        verbose_name_plural = "Eventi"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse('evento_detail', kwargs={'slug': self.slug})

    @property
    def is_past(self):
        from django.utils import timezone
        return self.data_inizio < timezone.now()


class Notizia(TranslatableModel):
    slug = models.SlugField(max_length=200, unique=True)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    immagine = models.ImageField(upload_to="notizie/", blank=True, null=True, help_text="Immagine principale della notizia.")
    is_active = models.BooleanField(default=True, help_text="Se la notizia è attiva e visibile.")

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200),
        contenuto=models.TextField(help_text="Contenuto completo della notizia."),
        riassunto=models.TextField(blank=True, null=True, help_text="Riassunto breve per le liste (opzionale)."),
    )

    class Meta:
        ordering = ['-data_pubblicazione']
        verbose_name = "Notizia"
        verbose_name_plural = "Notizie"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse('notizia_detail', kwargs={'slug': self.slug})


class Documento(TranslatableModel):
    """
    Modello per documenti e studi pubblicati dal Parco Letterario.
    Solo gli admin possono creare e modificare questi documenti.
    """
    slug = models.SlugField(max_length=200, unique=True)
    data_pubblicazione = models.DateTimeField(auto_now_add=True)
    anno_pubblicazione = models.IntegerField(null=True, blank=True, help_text="Anno di pubblicazione del documento/studio.")
    pdf_file = models.FileField(upload_to="documenti/", help_text="File PDF del documento o studio.")
    anteprima = models.ImageField(upload_to="documenti/anteprime/", blank=True, null=True, help_text="Immagine di anteprima del documento (copertina o prima pagina).")
    is_active = models.BooleanField(default=True, help_text="Se il documento è attivo e visibile.")
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('documento', 'Documento'),
            ('studio', 'Studio'),
            ('ricerca', 'Ricerca'),
            ('saggio', 'Saggio'),
        ],
        default='documento',
        help_text="Tipo di documento/studio."
    )
    autori = models.CharField(
        max_length=300,
        blank=True,
        null=True,
        help_text="Autori del documento/studio (es: 'Mario Rossi, Luigi Bianchi')."
    )

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200, help_text="Titolo del documento o studio."),
        descrizione=models.TextField(help_text="Descrizione dettagliata del contenuto del documento."),
        riassunto=models.TextField(
            blank=True,
            null=True,
            help_text="Riassunto breve per le liste (opzionale)."
        ),
        parole_chiave=models.CharField(
            max_length=300,
            blank=True,
            null=True,
            help_text="Parole chiave separate da virgola (opzionale)."
        ),
    )

    class Meta:
        ordering = ['-data_pubblicazione']
        verbose_name = "Documento"
        verbose_name_plural = "Documenti e Studi"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        return reverse('documento_detail', kwargs={'slug': self.slug})


class FotoArchivio(TranslatableModel):
    """
    Modello per le foto dell'archivio fotografico.
    Solo gli admin possono aggiungere foto.
    """
    immagine = models.ImageField(
        upload_to="archivio_fotografico/",
        help_text="Carica la foto per l'archivio."
    )
    data_aggiunta = models.DateTimeField(auto_now_add=True)
    ordine = models.IntegerField(
        default=0,
        help_text="Ordine di visualizzazione (numero più basso = prima)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Se la foto è attiva e visibile."
    )
    categoria = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Categoria della foto (es: 'Luoghi', 'Eventi', 'Personaggi')."
    )

    translations = TranslatedFields(
        titolo=models.CharField(
            max_length=200,
            blank=True,
            null=True,
            help_text="Titolo della foto (opzionale)."
        ),
        descrizione=models.TextField(
            blank=True,
            null=True,
            help_text="Descrizione della foto (opzionale)."
        ),
    )

    class Meta:
        ordering = ['ordine', '-data_aggiunta']
        verbose_name = "Foto Archivio"
        verbose_name_plural = "Archivio Fotografico"

    def __str__(self):
        titolo = self.safe_translation_getter('titolo', any_language=True)
        if titolo:
            return titolo
        return f"Foto #{self.pk}"


class Itinerario(TranslatableModel):
    """
    Modello per gli itinerari verghiani e capuaniani.
    """
    slug = models.SlugField(max_length=200, unique=True)
    immagine = models.ImageField(
        upload_to="itinerari/",
        help_text="Immagine rappresentativa dell'itinerario."
    )
    link_maps = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Link al percorso su Google Maps (opzionale)"
    )
    # Campi per la mappa interattiva
    coordinate_tappe = models.JSONField(
        blank=True,
        null=True,
        help_text="JSON con le coordinate delle tappe: [{'nome': 'Tappa 1', 'coords': [lat, lng], 'descrizione': '...', 'order': 1}, ...]"
    )
    colore_percorso = models.CharField(
        max_length=7,
        default='#2E7D32',
        help_text="Colore del percorso sulla mappa (formato hex, es: #2E7D32)"
    )
    icona_percorso = models.CharField(
        max_length=10,
        default='📖',
        help_text="Emoji/icona per il percorso (es: 📖, 🏛️, 🍷)"
    )
    durata_stimata = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Durata stimata (es: '2-3 ore', 'Mezza giornata')"
    )
    difficolta = models.CharField(
        max_length=50,
        choices=[
            ('facile', 'Facile'),
            ('media', 'Media'),
            ('difficile', 'Difficile'),
        ],
        default='facile',
        help_text="Difficoltà del percorso"
    )
    ordine = models.IntegerField(
        default=0,
        help_text="Ordine di visualizzazione (numero più basso = prima)."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Se l'itinerario è attivo e visibile."
    )
    tipo = models.CharField(
        max_length=50,
        choices=[
            ('verghiano', 'Itinerario Verghiano'),
            ('capuaniano', 'Itinerario Capuaniano'),
            ('tematico', 'Itinerario Tematico'),
        ],
        default='verghiano',
        help_text="Tipo di itinerario."
    )

    translations = TranslatedFields(
        titolo=models.CharField(max_length=200, help_text="Titolo dell'itinerario."),
        descrizione=models.TextField(help_text="Descrizione dettagliata dell'itinerario."),
    )

    class Meta:
        ordering = ['ordine', 'slug']
        verbose_name = "Itinerario"
        verbose_name_plural = "Itinerari"

    def __str__(self):
        return self.safe_translation_getter('titolo', any_language=True) or str(self.pk)

    def get_absolute_url(self):
        """Return the detail URL for this itinerario."""
        return reverse('itinerario_detail', kwargs={'slug': self.slug})


class TappaItinerario(TranslatableModel):
    """
    Modello per le singole tappe di un itinerario.
    """
    itinerario = models.ForeignKey(
        Itinerario,
        on_delete=models.CASCADE,
        related_name='tappe',
        help_text="Itinerario a cui appartiene questa tappa."
    )
    ordine = models.IntegerField(
        default=0,
        help_text="Ordine della tappa nell'itinerario (numero più basso = prima)."
    )
    immagine = models.ImageField(
        upload_to="tappe_itinerari/",
        blank=True,
        null=True,
        help_text="Immagine rappresentativa della tappa (opzionale)."
    )

    translations = TranslatedFields(
        nome=models.CharField(
            max_length=200,
            help_text="Nome della tappa (es. 'Tappa 1: Chiesa di Santa Margherita')"
        ),
        descrizione=models.TextField(
            help_text="Descrizione dettagliata della tappa."
        ),
    )

    class Meta:
        ordering = ['ordine']
        verbose_name = "Tappa Itinerario"
        verbose_name_plural = "Tappe Itinerari"

    def __str__(self):
        nome = self.safe_translation_getter('nome', any_language=True)
        itinerario_nome = self.itinerario.safe_translation_getter('titolo', any_language=True) if self.itinerario else 'N/A'
        return f"{itinerario_nome} - {nome}" if nome else f"Tappa #{self.pk}"


class Prenotazione(models.Model):
    """Modello per salvare le prenotazioni dal form della homepage"""
    LUOGO_CHOICES = [
        ('vizzini', 'Vizzini'),
        ('mineo', 'Mineo'),
        ('licodia', 'Licodia Eubea'),
    ]
    
    ITINERARIO_CHOICES = [
        ('verghiani', 'Itinerari verghiani'),
        ('capuaniani', 'Itinerari capuaniani'),
        ('tematici', 'Itinerari tematici'),
    ]
    
    PRIORITA_CHOICES = [
        ('bassa', 'Bassa'),
        ('media', 'Media'),
        ('alta', 'Alta'),
    ]
    
    STATO_CHOICES = [
        ('nuova', 'Nuova richiesta'),
        ('in_lavorazione', 'In lavorazione'),
        ('confermata', 'Confermata'),
        ('completata', 'Completata'),
        ('cancellata', 'Cancellata'),
    ]
    
    # Dati contatto
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cognome = models.CharField(max_length=100, verbose_name="Cognome")
    email = models.EmailField(verbose_name="Email")
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Telefono", help_text="Opzionale ma consigliato per contatto rapido")
    
    # Dettagli richiesta
    luogo = models.CharField(max_length=20, choices=LUOGO_CHOICES, verbose_name="Luogo")
    itinerario = models.CharField(max_length=20, choices=ITINERARIO_CHOICES, verbose_name="Tipologia itinerario")
    data_preferita = models.DateField(null=True, blank=True, verbose_name="Data preferita visita", help_text="Opzionale")
    numero_partecipanti = models.PositiveIntegerField(default=1, verbose_name="Numero partecipanti", help_text="Numero persone che parteciperanno")
    messaggio = models.TextField(blank=True, verbose_name="Messaggio/Richieste particolari", help_text="Eventuali richieste o informazioni aggiuntive")
    
    # Gestione amministrativa
    data_richiesta = models.DateTimeField(auto_now_add=True, verbose_name="Data richiesta")
    evasa = models.BooleanField(default=False, verbose_name="Evasa", help_text="Deprecato: usa campo 'stato'")
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='nuova', verbose_name="Stato", db_index=True)
    priorita = models.CharField(max_length=10, choices=PRIORITA_CHOICES, default='media', verbose_name="Priorità", db_index=True)
    
    # Gestione date
    data_completamento = models.DateTimeField(null=True, blank=True, verbose_name="Data completamento", help_text="Quando il servizio è stato erogato")
    data_evasione = models.DateTimeField(null=True, blank=True, verbose_name="Data evasione", help_text="Deprecato: usa data_completamento")
    
    # Team e note
    responsabile = models.CharField(max_length=100, blank=True, verbose_name="Responsabile", help_text="Chi ha gestito la richiesta")
    guida_assegnata = models.CharField(max_length=100, blank=True, verbose_name="Guida assegnata", help_text="Nome della guida turistica assegnata")
    note_admin = models.TextField(blank=True, verbose_name="Note amministratore", help_text="Note interne per il follow-up")
    
    # Metadati
    ultima_modifica = models.DateTimeField(auto_now=True, verbose_name="Ultima modifica")
    
    class Meta:
        ordering = ['-data_richiesta']
        verbose_name = "Prenotazione"
        verbose_name_plural = "Prenotazioni"
    
    def __str__(self):
        stato = "[OK]" if self.evasa else "[--]"
        return f"{stato} {self.nome} {self.cognome} - {self.get_luogo_display()} ({self.numero_partecipanti}p)"
    
    def save(self, *args, **kwargs):
        from django.utils import timezone
        
        # Sincronizza campo evasa con stato (retrocompatibilità)
        if self.stato in ['completata', 'cancellata']:
            self.evasa = True
        
        # Auto-update data completamento
        if self.stato == 'completata' and not self.data_completamento:
            self.data_completamento = timezone.now()
            if not self.data_evasione:
                self.data_evasione = timezone.now()
        
        # Backward compatibility
        if self.evasa and not self.data_evasione:
            self.data_evasione = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def giorni_attesa(self):
        """Calcola i giorni di attesa dalla richiesta"""
        from django.utils import timezone
        if self.stato in ['completata', 'cancellata']:
            data_fine = self.data_completamento or self.data_evasione or timezone.now()
        else:
            data_fine = timezone.now()
        return (data_fine.date() - self.data_richiesta.date()).days
    
    @property
    def in_ritardo(self):
        """Verifica se la prenotazione è in ritardo"""
        if self.stato in ['completata', 'cancellata']:
            return False
        if self.data_preferita:
            from django.utils import timezone
            return self.data_preferita < timezone.now().date() and self.stato != 'confermata'
        return False
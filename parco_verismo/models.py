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
        ordering = ['translations__titolo']
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
        ordering = ['ordine', 'translations__titolo']
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
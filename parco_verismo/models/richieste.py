"""
Modelli per il sistema di Richieste.
"""

# Django imports
from django.db import models
from django.utils.translation import gettext_lazy as _


class Richiesta(models.Model):
    """Modello per salvare le richieste dal form della homepage"""

    PRIORITA_CHOICES = [
        ("bassa", _("Bassa")),
        ("media", _("Media")),
        ("alta", _("Alta")),
    ]

    STATO_CHOICES = [
        ("nuova", _("Nuova richiesta")),
        ("in_lavorazione", _("In lavorazione")),
        ("confermata", _("Confermata")),
        ("completata", _("Completata")),
        ("cancellata", _("Cancellata")),
    ]

    # Dati contatto
    nome = models.CharField(max_length=100, verbose_name=_("Nome"))
    cognome = models.CharField(max_length=100, verbose_name=_("Cognome"))
    email = models.EmailField(verbose_name=_("Email"))

    # Messaggio
    messaggio = models.TextField(
        blank=False,
        verbose_name=_("Messaggio/Richieste particolari"),
        help_text=_("Inserisci il contenuto del messaggio (obbligatorio)"),
    )

    # Gestione amministrativa
    data_richiesta = models.DateTimeField(auto_now_add=True, verbose_name=_("Data richiesta"))
    stato = models.CharField(
        max_length=20, choices=STATO_CHOICES, default="nuova", verbose_name=_("Stato"), db_index=True
    )
    priorita = models.CharField(
        max_length=10, choices=PRIORITA_CHOICES, default="media", verbose_name=_("Priorità"), db_index=True
    )

    # Gestione date
    data_completamento = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Data completamento"),
        help_text=_("Quando il servizio è stato erogato"),
    )

    # Team e note
    ente = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_("Ente / Istituzione"),
        help_text=_("Facoltativo"),
    )
    oggetto = models.CharField(
        max_length=200,
        blank=False,
        verbose_name=_("Oggetto"),
        help_text=_("Oggetto della richiesta (obbligatorio)"),
    )
    responsabile = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Responsabile",
        help_text="Chi ha gestito la richiesta",
    )
    guida_assegnata = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Guida assegnata",
        help_text="Nome della guida turistica assegnata",
    )
    note_admin = models.TextField(
        blank=True,
        verbose_name="Note amministratore",
        help_text="Note interne per il follow-up",
    )

    # Metadati
    ultima_modifica = models.DateTimeField(auto_now=True, verbose_name="Ultima modifica")

    class Meta:
        ordering = ["-data_richiesta"]
        verbose_name = "Richiesta di contatto"
        verbose_name_plural = "Richieste di contatto"

    def __str__(self):
        stato_emoji = {
            "nuova": "🆕",
            "in_lavorazione": "⏳",
            "confermata": "✅",
            "completata": "✔️",
            "cancellata": "❌",
        }
        emoji = stato_emoji.get(self.stato, "📋")
        descr = self.oggetto if self.oggetto else "Richiesta"
        return f"{emoji} {self.nome} {self.cognome} - {descr}"

    def save(self, *args, **kwargs):
        from django.utils import timezone

        # Auto-update data completamento quando stato diventa completata
        if self.stato == "completata" and not self.data_completamento:
            self.data_completamento = timezone.now()

        super().save(*args, **kwargs)

    @property
    def giorni_attesa(self):
        """Calcola i giorni di attesa dalla richiesta"""
        from django.utils import timezone

        if self.stato in ["completata", "cancellata"]:
            data_fine = self.data_completamento or timezone.now()
        else:
            data_fine = timezone.now()
        return (data_fine.date() - self.data_richiesta.date()).days

    @property
    def in_ritardo(self):
        """Verifica se la richiesta è in ritardo (semplice heuristic)"""
        if self.stato in ["completata", "cancellata"]:
            return False
        # Se non abbiamo una data preferita, non possiamo determinare ritardo
        return False

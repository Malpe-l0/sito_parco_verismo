"""
Form per validazione Richieste.
"""

# Standard library imports
import re

# Django imports
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _

# Local imports
from ..models import Richiesta


class RichiestaForm(forms.ModelForm):
    """Form semplificato per il modulo di contatto pubblico"""

    class Meta:
        model = Richiesta
        fields = ["nome", "cognome", "email", "ente", "oggetto", "messaggio"]
        widgets = {
            "nome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Mario",
                    "required": True,
                    "minlength": "2",
                    "maxlength": "100",
                }
            ),
            "cognome": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Rossi",
                    "required": True,
                    "minlength": "2",
                    "maxlength": "100",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "mario.rossi@example.com",
                    "required": True,
                }
            ),
            "ente": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Nome ente o istituzione (facoltativo)"),
                }
            ),
            "oggetto": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Oggetto del messaggio"),
                    "required": True,
                }
            ),
            "messaggio": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "6",
                    "placeholder": _("Scrivi qui il tuo messaggio..."),
                    "maxlength": "1000",
                    "required": True,
                }
            ),
        }

    def clean_nome(self):
        """Validazione campo nome"""
        nome = self.cleaned_data.get("nome", "").strip()
        if not nome:
            raise ValidationError(_("Il nome è obbligatorio"))
        if len(nome) < 2:
            raise ValidationError(_("Il nome deve contenere almeno 2 caratteri"))
        if len(nome) > 100:
            raise ValidationError(_("Il nome non può superare 100 caratteri"))
        # Rimuovi caratteri non validi
        if not re.match(r"^[a-zA-ZàèéìòùÀÈÉÌÒÙ\s\'-]+$", nome):
            raise ValidationError(_("Il nome contiene caratteri non validi"))
        return nome.title()

    def clean_cognome(self):
        """Validazione campo cognome"""
        cognome = self.cleaned_data.get("cognome", "").strip()
        if not cognome:
            raise ValidationError(_("Il cognome è obbligatorio"))
        if len(cognome) < 2:
            raise ValidationError(_("Il cognome deve contenere almeno 2 caratteri"))
        if len(cognome) > 100:
            raise ValidationError(_("Il cognome non può superare 100 caratteri"))
        # Rimuovi caratteri non validi
        if not re.match(r"^[a-zA-ZàèéìòùÀÈÉÌÒÙ\s\'-]+$", cognome):
            raise ValidationError(_("Il cognome contiene caratteri non validi"))
        return cognome.title()

    def clean_email(self):
        """Validazione e normalizzazione email"""
        email = self.cleaned_data.get("email", "").strip().lower()
        if not email:
            raise ValidationError(_("L'email è obbligatoria"))

        # Validazione formato email
        validator = EmailValidator(message=_("Inserisci un indirizzo email valido"))
        try:
            validator(email)
        except ValidationError:
            raise ValidationError(
                _("Inserisci un indirizzo email valido (es: nome@dominio.it)")
            )

        # Blocca email temporanee/sospette (opzionale)
        domini_bloccati = ["tempmail.com", "throwaway.email", "10minutemail.com"]
        dominio = email.split("@")[1] if "@" in email else ""
        if dominio in domini_bloccati:
            raise ValidationError(_("Non sono accettate email temporanee"))

        return email

    def clean_messaggio(self):
        """Validazione messaggio"""
        messaggio = self.cleaned_data.get("messaggio", "").strip()
        if not messaggio:
            raise ValidationError(_("Il messaggio è obbligatorio"))
        if len(messaggio) > 1000:
            raise ValidationError(_("Il messaggio non può superare 1000 caratteri"))
        return messaggio

    def clean(self):
        """Validazione complessiva del form (anti-spam)"""
        cleaned_data = super().clean()

        messaggio = cleaned_data.get("messaggio", "")
        if messaggio:
            # Blocca messaggi con troppi link
            num_link = len(re.findall(r"https?://", messaggio))
            if num_link > 3:
                raise ValidationError(
                    _("Il messaggio contiene troppi link. Inserisci massimo 3 link.")
                )
            # Blocca messaggi solo maiuscole (spam comune)
            if len(messaggio) > 20 and messaggio.isupper():
                raise ValidationError(_("Non scrivere il messaggio tutto in maiuscolo"))

        # Validazione base su nome/cognome/email/oggetto/messaggio
        nome = cleaned_data.get("nome", "").strip()
        cognome = cleaned_data.get("cognome", "").strip()
        email = cleaned_data.get("email", "").strip()
        oggetto = cleaned_data.get("oggetto", "").strip()
        messaggio = cleaned_data.get("messaggio", "").strip()
        if not nome or len(nome) < 2:
            raise ValidationError(_("Inserisci un nome valido (almeno 2 caratteri)"))
        if not cognome or len(cognome) < 2:
            raise ValidationError(_("Inserisci un cognome valido (almeno 2 caratteri)"))
        if not email:
            raise ValidationError(_("L'email è obbligatoria"))
        if not oggetto:
            raise ValidationError(_("L'oggetto è obbligatorio"))
        if not messaggio:
            raise ValidationError(_("Il messaggio è obbligatorio"))

        return cleaned_data

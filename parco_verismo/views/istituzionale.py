# Django imports
# Django imports
import logging
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Local imports
from ..forms.richiesta import RichiestaForm


def _get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _check_contatti_rate_limit(ip):
    """Permette al massimo 3 invii per ora per IP sulla pagina contatti."""
    cache_key = f"contatti_rl:{ip}"
    count = cache.get(cache_key, 0)
    if count >= 3:
        return False
    cache.set(cache_key, count + 1, 3600)
    return True


# =============================================================================
# VIEWS ISTITUZIONALI E INFORMATIVE
# =============================================================================


def missione_visione_view(request):
    """Pagina Missione e Visione del Parco Letterario."""
    return render(request, "parco_verismo/missione_visione.html")


def comitato_tecnico_scientifico_view(request):
    """Pagina del Comitato Tecnico-Scientifico del Parco Letterario."""
    return render(request, "parco_verismo/comitato_tecnico_scientifico.html")


def comitato_regolamento_view(request):
    """Pagina del regolamento del Comitato Tecnico-Scientifico."""
    return render(request, "parco_verismo/comitato_regolamento.html")
def regolamenti_documenti_view(request):
    """Pagina Regolamenti e Documenti del Parco."""
    return render(request, "parco_verismo/regolamenti_documenti.html")


def partner_rete_territoriale_view(request):
    """Pagina Partner e Rete Territoriale."""
    return render(request, "parco_verismo/partner_rete_territoriale.html")


def accrediti_finanziamenti_view(request):
    """Pagina Accrediti e Finanziamenti."""
    return render(request, "parco_verismo/accrediti_finanziamenti.html")


def contatti_view(request):
    """Pagina Contatti del Parco Letterario con modulo funzionale."""
    if request.method == "POST":
        # Rate limit: max 3 invii per ora per IP
        ip = _get_client_ip(request)
        if not _check_contatti_rate_limit(ip):
            messages.error(
                request,
                "Hai inviato troppe richieste. Riprova tra un'ora."
            )
            return render(request, "parco_verismo/contatti.html", {"form": RichiestaForm()})

        form = RichiestaForm(request.POST)
        if form.is_valid():
            # Honeypot: se compilato è un bot — simula successo senza salvare
            if form.cleaned_data.get("website"):
                logging.warning("Honeypot attivato da IP=%s", ip)
                messages.success(
                    request,
                    "Messaggio inviato con successo! Ti contatteremo al più presto."
                )
                return HttpResponseRedirect(reverse("contatti") + "#richiesta-contatto")

            try:
                richiesta = form.save()
                
                # Invia email di notifica
                try:
                    from django.core.mail import send_mail
                    from django.conf import settings
                    
                    subject = f"Nuova richiesta dal sito: {richiesta.oggetto}"
                    message = f"""
Hai ricevuto una nuova richiesta di contatto dal sito web.

Dettagli:
Nome: {richiesta.nome} {richiesta.cognome}
Email: {richiesta.email}
Ente: {richiesta.ente or 'Non specificato'}
Oggetto: {richiesta.oggetto}

Messaggio:
{richiesta.messaggio}

Puoi gestire questa richiesta dal pannello di amministrazione:
{request.scheme}://{request.get_host()}/richieste/dashboard/
                    """
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,  # Mittente (configurato in settings)
                        ["info@parcovergacapuana.it"],  # Destinatario
                        fail_silently=False,
                    )
                except Exception as e:
                    logging.error(f"Errore invio email: {e}")
                    # Non blocchiamo il flusso se l'email fallisce, ma logghiamo l'errore

                logging.info(
                    "Richiesta contatto creata id=%s email=%s",
                    getattr(richiesta, "id", "unknown"),
                    richiesta.email,
                )
                messages.success(
                    request,
                    "Messaggio inviato con successo! Ti contatteremo al più presto."
                )
                return HttpResponseRedirect(reverse("contatti") + "#richiesta-contatto")
            except Exception:
                logging.exception("Errore nel salvataggio della richiesta contatti")
                messages.error(request, "Errore nel salvataggio. Riprova più tardi.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    if field == "__all__":
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f"{field_label}: {error}")
    else:
        form = RichiestaForm()

    return render(request, "parco_verismo/contatti.html", {"form": form})


# =============================================================================
# VIEWS PER CONFORMITÀ GDPR E PA
# =============================================================================


def privacy_policy_view(request):
    """Pagina Privacy Policy conforme GDPR."""
    return render(request, "parco_verismo/privacy_policy.html")


def note_legali_view(request):
    """Pagina Note Legali per PA."""
    return render(request, "parco_verismo/note_legali.html")


def cookie_policy_view(request):
    """Pagina Cookie Policy."""
    return render(request, "parco_verismo/cookie_policy.html")

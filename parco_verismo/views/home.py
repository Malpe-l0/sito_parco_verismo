"""
Views per la homepage.
"""
# Django imports
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils import timezone

# Local imports
from ..forms.prenotazione import PrenotazioneForm
from ..models import Evento, Notizia


def home_view(request):
    """Vista homepage con form prenotazione e contenuti in evidenza."""
    # Gestione form di contatto con validazione
    if request.method == 'POST':
        form = PrenotazioneForm(request.POST)
        if form.is_valid():
            try:
                prenotazione = form.save()
                messages.success(
                    request, 
                    'Prenotazione inviata con successo! Ti contatteremo presto via email.'
                )
                return redirect('home' + '#prenota-itinerario')
            except Exception as e:
                messages.error(request, 'Errore nel salvataggio. Riprova più tardi.')
        else:
            # Mostra errori di validazione
            for field, errors in form.errors.items():
                for error in errors:
                    if field == '__all__':
                        messages.error(request, error)
                    else:
                        field_label = form.fields[field].label or field
                        messages.error(request, f'{field_label}: {error}')
    else:
        form = PrenotazioneForm()

    # Eventi: prendere i prossimi eventi attivi (a partire da oggi) ordinati per data
    eventi_latest = Evento.objects.filter(is_active=True, data_inizio__gte=timezone.now()).order_by('data_inizio')[:4]

    # Notizie: prendere le ultime notizie attive ordinate per data di pubblicazione
    notizie_latest = Notizia.objects.filter(is_active=True).order_by('-data_pubblicazione')[:4]

    context = {
        'eventi': eventi_latest,
        'notizie': notizie_latest,
        'oggi': timezone.now().date().isoformat(),
    }
    return render(request, 'parco_verismo/index.html', context)

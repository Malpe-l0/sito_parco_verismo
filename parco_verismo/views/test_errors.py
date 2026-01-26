"""
NOTA: Questo file è solo per testare le pagine di errore in sviluppo.
NON usare in produzione!

Per testare le pagine di errore, aggiungi temporaneamente queste URL al tuo urls.py:

from parco_verismo.views.test_errors import (
    test_404_view,
    test_500_view,
    test_403_view,
    test_400_view,
)

urlpatterns += [
    path('test-404/', test_404_view, name='test_404'),
    path('test-500/', test_500_view, name='test_500'),
    path('test-403/', test_403_view, name='test_403'),
    path('test-400/', test_400_view, name='test_400'),
]

Poi visita:
- http://127.0.0.1:8000/test-404/
- http://127.0.0.1:8000/test-500/
- http://127.0.0.1:8000/test-403/
- http://127.0.0.1:8000/test-400/
"""
from django.shortcuts import render
from django.http import HttpResponse


def test_404_view(request):
    """Test della pagina 404"""
    return render(request, '404.html', status=404)


def test_500_view(request):
    """Test della pagina 500"""
    return render(request, '500.html', status=500)


def test_403_view(request):
    """Test della pagina 403"""
    return render(request, '403.html', status=403)


def test_400_view(request):
    """Test della pagina 400"""
    return render(request, '400.html', status=400)

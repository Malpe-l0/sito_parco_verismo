"""
Custom error handlers per le pagine di errore HTTP.
"""
from django.shortcuts import render


def custom_404(request, exception=None):
    """
    Handler personalizzato per errore 404 - Pagina non trovata.
    
    Args:
        request: HttpRequest
        exception: L'eccezione che ha causato l'errore 404
        
    Returns:
        HttpResponse con status code 404
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Handler personalizzato per errore 500 - Errore del server.
    
    Args:
        request: HttpRequest
        
    Returns:
        HttpResponse con status code 500
    """
    return render(request, '500.html', status=500)


def custom_403(request, exception=None):
    """
    Handler personalizzato per errore 403 - Accesso negato.
    
    Args:
        request: HttpRequest
        exception: L'eccezione che ha causato l'errore 403
        
    Returns:
        HttpResponse con status code 403
    """
    return render(request, '403.html', status=403)


def custom_400(request, exception=None):
    """
    Handler personalizzato per errore 400 - Richiesta non valida.
    
    Args:
        request: HttpRequest
        exception: L'eccezione che ha causato l'errore 400
        
    Returns:
        HttpResponse con status code 400
    """
    return render(request, '400.html', status=400)

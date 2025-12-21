"""
Views di utilità per il sistema.
"""

from django.http import JsonResponse


def health_check_view(request):
    """
    Endpoint di health check per Docker e Nginx.
    Utilizzato per verificare che l'applicazione sia in esecuzione.
    """
    return JsonResponse({
        "status": "healthy",
        "service": "parco-verismo",
    })

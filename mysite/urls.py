"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('parco_verismo/', include('parco_verismo.urls'))
"""

# Django imports
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.http import HttpResponse

# Local imports

from parco_verismo.sitemaps import (
    StaticViewSitemap,
    OperaSitemap,
    AutoreSitemap,
    EventoSitemap,
    NotiziaSitemap,
    DocumentoSitemap,
    ItinerarioSitemap,
)
# Custom admin site for public richieste dashboard
from parco_verismo.admin_richieste import richieste_admin_site

# Configurazione Sitemap per SEO
sitemaps = {
    "static": StaticViewSitemap,
    "opere": OperaSitemap,
    "autori": AutoreSitemap,
    "eventi": EventoSitemap,
    "notizie": NotiziaSitemap,
    "documenti": DocumentoSitemap,
    "itinerari": ItinerarioSitemap,
}

# Health check endpoint per Docker
def health_check(request):
    return HttpResponse("ok", content_type="text/plain")

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("health/", health_check, name="health_check"),
]

# URL con prefisso lingua (it/en)
urlpatterns += i18n_patterns(
    path("", include("parco_verismo.urls")),
    prefix_default_language=False,
)

# Admin senza prefisso lingua
urlpatterns += [
    path("admin/", admin.site.urls),
    # Dashboard per la gestione delle richieste (admin semplificato)
    path("richieste/", richieste_admin_site.urls),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # Root-level SEO files
    path("favicon.ico", lambda r: HttpResponse(open(settings.BASE_DIR / "parco_verismo/static/assets/img/favicon.ico", "rb").read(), content_type="image/x-icon")),
    path("robots.txt", lambda r: HttpResponse(open(settings.BASE_DIR / "parco_verismo/static/robots.txt", "r").read(), content_type="text/plain")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'parco_verismo.views.errors.custom_404'
handler500 = 'parco_verismo.views.errors.custom_500'
handler403 = 'parco_verismo.views.errors.custom_403'
handler400 = 'parco_verismo.views.errors.custom_400'

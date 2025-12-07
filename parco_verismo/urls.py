from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    # Pagina principale della biblioteca con ricerca
    path('biblioteca/', views.biblioteca_view, name='biblioteca'),
    
    # Pagine di presentazione per autore
    path('opere/<slug:autore_slug>/', views.opere_per_autore_view, name='opere_per_autore'),

    # Pagina di dettaglio/presentazione della singola opera
    path('opera/<slug:slug>/', views.opera_detail_view, name='opera_detail'),

    # Eventi e calendario
    path('eventi/', views.eventi_view, name='eventi'),
    path('calendario/', views.calendario_view, name='calendario'),
    path('evento/<slug:slug>/', views.evento_detail_view, name='evento_detail'),

    # Notizie
    path('notizie/', views.notizie_view, name='notizie'),
    path('notizia/<slug:slug>/', views.notizia_detail_view, name='notizia_detail'),

    # Documenti e Studi
    path('documenti/', views.documenti_view, name='documenti'),
    path('documento/<slug:slug>/', views.documento_detail_view, name='documento_detail'),

    # Archivio Fotografico
    path('archivio/', views.archivio_fotografico_view, name='archivio_fotografico'),

    # Pagine statiche per i comuni del Parco
    path('licodia/', views.licodia_view, name='licodia'),
    path('mineo/', views.mineo_view, name='mineo'),
    path('vizzini/', views.vizzini_view, name='vizzini'),

    # Missione e Visione
    path('missione-visione/', views.missione_visione_view, name='missione_visione'),

    # Comitato Tecnico-Scientifico
    path('comitato/', views.comitato_tecnico_scientifico_view, name='comitato_tecnico_scientifico'),
    path('comitato/regolamento/', views.comitato_regolamento_view, name='comitato_regolamento'),

    # Regolamenti e Documenti
    path('regolamenti-documenti/', views.regolamenti_documenti_view, name='regolamenti_documenti'),

    # Partner e Rete Territoriale
    path('partner/', views.partner_rete_territoriale_view, name='partner_rete_territoriale'),

    # Accrediti e Finanziamenti
    path('finanziamenti/', views.accrediti_finanziamenti_view, name='accrediti_finanziamenti'),
    
    # Itinerari (liste e dettaglio)
    path('itinerari/verghiani/', views.itinerari_verghiani_view, name='itinerari_verghiani'),
    path('itinerari/capuaniani/', views.itinerari_capuaniani_view, name='itinerari_capuaniani'),
    path('itinerari/tematici/', views.itinerari_tematici_view, name='itinerari_tematici'),
    path('itinerario/<slug:slug>/', views.itinerario_detail_view, name='itinerario_detail'),
    
    # Pagine di conformità GDPR e PA
    path('privacy/', views.privacy_policy_view, name='privacy_policy'),
    path('note-legali/', views.note_legali_view, name='note_legali'),
    path('cookie-policy/', views.cookie_policy_view, name='cookie_policy'),
    path('accessibilita/', views.dichiarazione_accessibilita_view, name='dichiarazione_accessibilita'),
]

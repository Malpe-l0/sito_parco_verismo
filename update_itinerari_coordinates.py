#!/usr/bin/env python3
"""
Script per aggiornare gli itinerari con coordinate per la mappa interattiva.

Esegui questo script con: python update_itinerari_coordinates.py
"""
import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Itinerario

def update_coordinates():
    print("="*70)
    print("AGGIORNAMENTO COORDINATE ITINERARI")
    print("="*70)
    
    # Esempio: Itinerario "Sulle tracce de I Malavoglia"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-malavoglia')
        itinerario.coordinate_tappe = [
            {
                "nome": "Aci Trezza - Casa del Nespolo",
                "coords": [37.5614, 15.1595],
                "descrizione": "La casa della famiglia Malavoglia, protagonista del romanzo",
                "order": 1
            },
            {
                "nome": "Faraglioni dei Ciclopi",
                "coords": [37.5589, 15.1642],
                "descrizione": "Gli iconici scogli di basalto, teatro delle vicende marinare",
                "order": 2
            },
            {
                "nome": "Chiesa di San Giovanni Battista",
                "coords": [37.5625, 15.1580],
                "descrizione": "La chiesa del paese dove la famiglia partecipava alle funzioni",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#1976D2'
        itinerario.icona_percorso = '🌊'
        itinerario.durata_stimata = '2 ore'
        itinerario.difficolta = 'facile'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-malavoglia' non trovato")
    
    # Esempio: Itinerario "Il mondo di Mastro-don Gesualdo"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-mastro-don-gesualdo')
        itinerario.coordinate_tappe = [
            {
                "nome": "Vizzini - Piazza Umberto I",
                "coords": [37.1584, 14.7443],
                "descrizione": "Il cuore del paese, scenario del romanzo",
                "order": 1
            },
            {
                "nome": "Palazzo Verga",
                "coords": [37.1578, 14.7438],
                "descrizione": "Dimora storica che ispirò lo scrittore",
                "order": 2
            },
            {
                "nome": "Chiesa di San Giovanni Battista",
                "coords": [37.1590, 14.7450],
                "descrizione": "Chiesa barocca frequentata dalla nobiltà locale",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#8B4513'
        itinerario.icona_percorso = '🏛️'
        itinerario.durata_stimata = '3 ore'
        itinerario.difficolta = 'facile'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-mastro-don-gesualdo' non trovato")
    
    # Esempio: Itinerario "I luoghi di Vita dei campi"
    try:
        itinerario = Itinerario.objects.get(slug='itinerario-vita-dei-campi')
        itinerario.coordinate_tappe = [
            {
                "nome": "Campagne di Vizzini",
                "coords": [37.1700, 14.7500],
                "descrizione": "Paesaggi rurali immutati nel tempo",
                "order": 1
            },
            {
                "nome": "Antica Masseria",
                "coords": [37.1650, 14.7600],
                "descrizione": "Esempio di architettura rurale siciliana",
                "order": 2
            },
            {
                "nome": "Bosco di Santo Pietro",
                "coords": [37.1550, 14.7700],
                "descrizione": "Area boschiva che fa da sfondo alle novelle",
                "order": 3
            }
        ]
        itinerario.colore_percorso = '#388E3C'
        itinerario.icona_percorso = '🌾'
        itinerario.durata_stimata = '4 ore'
        itinerario.difficolta = 'media'
        itinerario.save()
        print(f"✓ Aggiornato: {itinerario.titolo}")
    except Itinerario.DoesNotExist:
        print("✗ Itinerario 'itinerario-vita-dei-campi' non trovato")
    
    print("\n" + "="*70)
    print("AGGIORNAMENTO COMPLETATO!")
    print("="*70)

if __name__ == '__main__':
    update_coordinates()

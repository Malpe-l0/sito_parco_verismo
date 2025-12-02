#!/usr/bin/env python3
"""
Script per popolare il database con gli itinerari verghiani.

Esegui questo script con: python populate_itinerari.py
"""
import os
import django
from django.core.files import File
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Itinerario
from django.conf import settings

def copy_static_to_media(source_path, destination_relative):
    """
    Copia un file da static/assets/img a media/ e restituisce il percorso del file copiato
    """
    static_source = os.path.join(settings.BASE_DIR, 'parco_verismo', 'static', 'assets', 'img', source_path)
    media_dest = os.path.join(settings.MEDIA_ROOT, destination_relative)
    
    # Crea la directory se non esiste
    os.makedirs(os.path.dirname(media_dest), exist_ok=True)
    
    if os.path.exists(static_source):
        shutil.copy2(static_source, media_dest)
        return destination_relative
    return None

def populate_itinerari():
    print("="*70)
    print("POPOLAMENTO ITINERARI VERGHIANI")
    print("="*70)
    
    itinerari_data = [
        {
            'titolo': 'Sulle tracce de I Malavoglia',
            'slug': 'itinerario-malavoglia',
            'descrizione': '''Un percorso affascinante che ripercorre i luoghi narrati nel capolavoro 
verghiano "I Malavoglia". Il percorso parte da Aci Trezza, dove si può ammirare la casa del Nespolo 
e i Faraglioni dei Ciclopi, teatro delle vicende della famiglia Toscano. Il percorso si snoda tra 
le vie del borgo marinaro, toccando i luoghi dove Verga ambientò le sue storie più celebri.''',
            'tipo': 'verghiano',
            'ordine': 1,
            'immagine_path': 'vizzini/centrostorico.jpg',
            'is_active': True
        },
        {
            'titolo': 'Il mondo di Mastro-don Gesualdo',
            'slug': 'itinerario-mastro-don-gesualdo',
            'descrizione': '''Questo itinerario vi porta alla scoperta di Vizzini, città natale di Giovanni Verga 
e scenario principale del romanzo "Mastro-don Gesualdo". Si visiterà il palazzo nobiliare che ispirò 
lo scrittore, il centro storico con le sue chiese barocche e i luoghi che hanno fatto da sfondo alle 
vicende del protagonista. Un viaggio nella stratificazione sociale della Sicilia dell'Ottocento.''',
            'tipo': 'verghiano',
            'ordine': 2,
            'immagine_path': 'vizzini/borgo.jpg',
            'is_active': True
        },
        {
            'titolo': 'I luoghi di Vita dei campi',
            'slug': 'itinerario-vita-dei-campi',
            'descrizione': '''Un percorso attraverso le campagne siciliane che hanno ispirato le novelle 
di "Vita dei campi". Si attraversano campi coltivati, antiche masserie e paesaggi rurali immutati 
nel tempo, gli stessi che Verga descrisse con crudo realismo nelle sue opere. Un'immersione nella 
Sicilia contadina dell'Ottocento, tra tradizioni e fatiche quotidiane.''',
            'tipo': 'verghiano',
            'ordine': 3,
            'immagine_path': 'vizzini/bosco.jpeg',
            'is_active': True
        },
        {
            'titolo': 'Da Vizzini ad Aci Trezza',
            'slug': 'itinerario-vizzini-aci-trezza',
            'descrizione': '''Un percorso completo che collega Vizzini, città natale di Verga, ad Aci Trezza, 
scenario de "I Malavoglia". Un viaggio attraverso i paesaggi che hanno ispirato lo scrittore, toccando 
borghi storici, campagne e il mare. Questo itinerario offre una panoramica completa dei luoghi verghiani, 
dalle colline dell'entroterra fino alle coste del Mar Ionio.''',
            'tipo': 'verghiano',
            'ordine': 4,
            'immagine_path': 'vizzini/casaVerga.jpg',
            'is_active': True
        },
        {
            'titolo': 'La Cunziria e il centro storico',
            'slug': 'itinerario-cunziria',
            'descrizione': '''Un itinerario urbano attraverso il centro storico di Vizzini, con particolare 
attenzione alla Cunziria, l'antica conceria che rappresenta uno dei luoghi più caratteristici del paese. 
Il percorso tocca anche il Palazzo Verga, il Duomo e le vie che Verga percorreva quotidianamente. 
Un viaggio nella memoria dello scrittore e nella storia del borgo.''',
            'tipo': 'verghiano',
            'ordine': 5,
            'immagine_path': 'vizzini/cunziria.jpg',
            'is_active': True
        },
    ]
    
    for itinerario_data in itinerari_data:
        itinerario, created = Itinerario.objects.get_or_create(
            slug=itinerario_data['slug'],
            defaults={
                'tipo': itinerario_data['tipo'],
                'ordine': itinerario_data['ordine'],
                'is_active': itinerario_data.get('is_active', True)
            }
        )
        
        if not created:
            itinerario.tipo = itinerario_data['tipo']
            itinerario.ordine = itinerario_data['ordine']
            itinerario.is_active = itinerario_data.get('is_active', True)
        
        # Copia l'immagine se specificata e non esiste già
        if 'immagine_path' in itinerario_data and not itinerario.immagine:
            image_path = copy_static_to_media(
                itinerario_data['immagine_path'], 
                f"itinerari/{itinerario_data['slug']}.jpg"
            )
            if image_path:
                media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(media_path, 'rb') as f:
                    itinerario.immagine.save(f"{itinerario_data['slug']}.jpg", File(f), save=False)
        
        # Imposta i campi traducibili
        itinerario.set_current_language('it')
        itinerario.titolo = itinerario_data['titolo']
        itinerario.descrizione = itinerario_data['descrizione']
        itinerario.save()
        
        if created:
            print(f"✓ Creato itinerario: {itinerario.titolo}")
        else:
            print(f"• Itinerario aggiornato: {itinerario.titolo}")
    
    print("\n" + "="*70)
    print("POPOLAMENTO ITINERARI COMPLETATO!")
    print("="*70)
    print(f"\nTotale itinerari: {Itinerario.objects.count()}")
    print(f"Itinerari verghiani: {Itinerario.objects.filter(tipo='verghiano').count()}")
    print(f"\nPuoi visualizzare gli itinerari su:")
    print("  http://127.0.0.1:8000/itinerari-verghiani/")

if __name__ == '__main__':
    populate_itinerari()

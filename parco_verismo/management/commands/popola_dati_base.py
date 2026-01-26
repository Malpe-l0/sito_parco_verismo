"""
Management command per popolare il database con dati di base.
Uso: python manage.py popola_dati_base
"""

from django.core.management.base import BaseCommand
from django.utils import translation
from parco_verismo.models import Autore, Opera
from datetime import datetime


class Command(BaseCommand):
    help = 'Popola il database con autori e opere di base'

    def handle(self, *args, **options):
        # Attiva la lingua italiana per le traduzioni
        translation.activate('it')
        
        self.stdout.write(self.style.SUCCESS('Inizio popolamento dati di base...'))
        
        # Crea autori
        verga, created = Autore.objects.get_or_create(
            nome='Giovanni Verga',
            defaults={'slug': 'giovanni-verga'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Autore creato: {verga.nome}'))
        else:
            self.stdout.write(self.style.WARNING(f'  Autore già esistente: {verga.nome}'))
        
        capuana, created = Autore.objects.get_or_create(
            nome='Luigi Capuana',
            defaults={'slug': 'luigi-capuana'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ Autore creato: {capuana.nome}'))
        else:
            self.stdout.write(self.style.WARNING(f'  Autore già esistente: {capuana.nome}'))
        
        # Opere di Verga
        opere_verga = [
            {
                'titolo': 'I Malavoglia',
                'anno': 1881,
                'trama': 'Il romanzo narra le vicende della famiglia Toscano, soprannominata "Malavoglia", una famiglia di pescatori di Aci Trezza. La narrazione segue le sventure che colpiscono la famiglia dopo la morte di Bastianazzo e la perdita della casa del nespolo, simbolo della stabilità familiare.',
                'analisi': 'Capolavoro del verismo italiano, il romanzo rappresenta il mondo arcaico e immobile dei pescatori siciliani, destinato a soccombere di fronte al progresso. Verga utilizza il discorso indiretto libero per far emergere la voce corale del paese.',
                'link': 'https://it.wikisource.org/wiki/I_Malavoglia'
            },
            {
                'titolo': 'Mastro-don Gesualdo',
                'anno': 1889,
                'trama': 'La storia di Gesualdo Motta, un muratore che attraverso il lavoro e l\'astuzia riesce ad arricchirsi, ma non trova mai pace né accettazione nella società nobiliare a cui ambisce appartenere.',
                'analisi': 'Secondo romanzo del "Ciclo dei Vinti", rappresenta il dramma dell\'uomo che, pur conquistando ricchezza, non riesce a superare le barriere sociali del suo tempo. L\'opera analizza il tema della lotta per l\'ascesa sociale e della solitudine esistenziale.',
                'link': 'https://it.wikisource.org/wiki/Mastro-don_Gesualdo'
            },
            {
                'titolo': 'Vita dei campi',
                'anno': 1880,
                'trama': 'Raccolta di novelle che descrivono la vita dei contadini siciliani, con storie di passioni, gelosie e tragedie quotidiane. Include celebri novelle come "Cavalleria rusticana", "La lupa" e "Rosso Malpelo".',
                'analisi': 'Prima raccolta organica di novelle veriste di Verga. L\'autore abbandona definitivamente i temi romantici per concentrarsi sulla rappresentazione cruda e oggettiva della vita nelle campagne siciliane, applicando i principi del verismo letterario.',
                'link': 'https://it.wikisource.org/wiki/Vita_dei_campi_(Verga)'
            },
            {
                'titolo': 'Novelle rusticane',
                'anno': 1883,
                'trama': 'Seconda raccolta di novelle veriste, che approfondisce i temi della vita contadina siciliana, con storie che mostrano la durezza dell\'esistenza, l\'avidità e le passioni che animano i personaggi.',
                'analisi': 'Prosecuzione della poetica verista iniziata con "Vita dei campi". Le novelle presentano una rappresentazione ancora più amara e disillusa della società siciliana, evidenziando la lotta per la sopravvivenza e il peso delle convenzioni sociali.',
                'link': 'https://it.wikisource.org/wiki/Novelle_rusticane'
            }
        ]
        
        for opera_data in opere_verga:
            slug = opera_data['titolo'].lower().replace(' ', '-').replace("'", '')
            opera, created = Opera.objects.get_or_create(
                autore=verga,
                slug=slug,
                defaults={
                    'anno_pubblicazione': opera_data['anno'],
                    'link_wikisource': opera_data['link']
                }
            )
            
            if created:
                # Imposta le traduzioni in italiano
                opera.set_current_language('it')
                opera.titolo = opera_data['titolo']
                opera.trama = opera_data['trama']
                opera.analisi = opera_data['analisi']
                opera.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opera creata: {opera_data["titolo"]} ({opera_data["anno"]})'))
            else:
                self.stdout.write(self.style.WARNING(f'  Opera già esistente: {opera_data["titolo"]}'))
        
        # Opere di Capuana
        opere_capuana = [
            {
                'titolo': 'Giacinta',
                'anno': 1879,
                'trama': 'La storia di Giacinta, una giovane donna della nobiltà siciliana che, dopo aver subito una violenza nell\'infanzia, vive un\'esistenza tormentata tra matrimonio, adulterio e ricerca di redenzione.',
                'analisi': 'Considerato uno dei primi romanzi veristi italiani, l\'opera affronta temi scottanti come la sessualità femminile e il trauma psicologico, con un\'attenzione quasi clinica alla psicologia del personaggio.',
                'link': 'https://it.wikisource.org/wiki/Giacinta_(Capuana)'
            },
            {
                'titolo': 'Il marchese di Roccaverdina',
                'anno': 1901,
                'trama': 'Il marchese, dopo aver fatto uccidere per gelosia l\'amante della donna che ama, è tormentato dal rimorso che lo conduce alla follia e alla confessione.',
                'analisi': 'Capolavoro di Capuana, il romanzo unisce l\'analisi verista della società siciliana con un\'approfondita indagine psicologica del protagonista, mostrando gli effetti devastanti del senso di colpa.',
                'link': 'https://it.wikisource.org/wiki/Il_marchese_di_Roccaverdina'
            },
            {
                'titolo': 'Profumo',
                'anno': 1890,
                'trama': 'Raccolta di novelle che esplorano le passioni, i vizi e le virtù della società siciliana attraverso storie di personaggi comuni e aristocratici.',
                'analisi': 'Le novelle dimostrano la maestria di Capuana nel cogliere gli aspetti psicologici dei personaggi e nel rappresentare la complessità delle relazioni umane nella Sicilia di fine Ottocento.',
                'link': 'https://it.wikisource.org/wiki/Profumo_(Capuana)'
            }
        ]
        
        for opera_data in opere_capuana:
            slug = opera_data['titolo'].lower().replace(' ', '-').replace("'", '')
            opera, created = Opera.objects.get_or_create(
                autore=capuana,
                slug=slug,
                defaults={
                    'anno_pubblicazione': opera_data['anno'],
                    'link_wikisource': opera_data['link']
                }
            )
            
            if created:
                # Imposta le traduzioni in italiano
                opera.set_current_language('it')
                opera.titolo = opera_data['titolo']
                opera.trama = opera_data['trama']
                opera.analisi = opera_data['analisi']
                opera.save()
                self.stdout.write(self.style.SUCCESS(f'✓ Opera creata: {opera_data["titolo"]} ({opera_data["anno"]})'))
            else:
                self.stdout.write(self.style.WARNING(f'  Opera già esistente: {opera_data["titolo"]}'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(self.style.SUCCESS('Popolamento completato!'))
        self.stdout.write(self.style.SUCCESS('========================================'))
        self.stdout.write(f'Autori creati: {Autore.objects.count()}')
        self.stdout.write(f'Opere create: {Opera.objects.count()}')
        self.stdout.write('')
        self.stdout.write('Puoi ora accedere all\'admin per gestire questi contenuti:')
        self.stdout.write('http://127.0.0.1:8000/admin/')

#!/usr/bin/env python3
"""
Script completo per popolare il database con:
- Tutte le opere principali di Verga e Capuana con link Wikisource
- Eventi con foto
- Notizie con foto
- Archivio fotografico con foto esistenti del sito

Esegui questo script con: python populate_db_complete.py
"""
import os
import django
from datetime import datetime, timedelta
from django.core.files import File
import shutil

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from parco_verismo.models import Autore, Opera, Evento, Notizia, FotoArchivio
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
        # Restituisce il percorso relativo per usarlo con Django File
        return destination_relative
    return None

def populate():
    print("="*70)
    print("POPOLAMENTO COMPLETO DEL DATABASE")
    print("="*70)
    
    # ========================================================================
    # CREAZIONE AUTORI
    # ========================================================================
    print("\n" + "="*70)
    print("CREAZIONE AUTORI")
    print("="*70)
    
    verga, created = Autore.objects.get_or_create(
        slug='giovanni-verga',
        defaults={'nome': 'Giovanni Verga'}
    )
    if created:
        print(f"✓ Creato autore: {verga.nome}")
    else:
        print(f"• Autore già esistente: {verga.nome}")
    
    capuana, created = Autore.objects.get_or_create(
        slug='luigi-capuana',
        defaults={'nome': 'Luigi Capuana'}
    )
    if created:
        print(f"✓ Creato autore: {capuana.nome}")
    else:
        print(f"• Autore già esistente: {capuana.nome}")
    
    # ========================================================================
    # OPERE DI GIOVANNI VERGA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI GIOVANNI VERGA")
    print("="*70)
    
    opere_verga = [
        {
            'titolo': 'I Malavoglia',
            'slug': 'i-malavoglia',
            'anno_pubblicazione': 1881,
            'trama': '''I Malavoglia è un romanzo corale che narra le vicende della famiglia Toscano, 
soprannominati "Malavoglia", poveri pescatori del paese di Aci Trezza. La storia si concentra sui 
tentativi di Padron 'Ntoni di mantenere unita la famiglia e di ripagare un debito contratto per 
l'acquisto di una partita di lupini destinata al commercio. Il naufragio della barca "Provvidenza", 
che trasportava i lupini, segna l'inizio di una serie di disgrazie che colpiranno la famiglia.''',
            'analisi': '''L'opera è considerata il capolavoro del Verismo italiano. Verga descrive 
con realismo la vita dei pescatori siciliani, le loro lotte contro la miseria e il destino. 
Il romanzo è caratterizzato dall'uso del discorso indiretto libero e da una lingua che riflette 
il parlato popolare siciliano. Tema centrale è il contrasto tra il mondo tradizionale, rappresentato 
da Padron 'Ntoni, e le aspirazioni di modernità dei giovani.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/I_Malavoglia',
            'copertina_path': 'vizzini/centrostorico.jpg'
        },
        {
            'titolo': 'Mastro-don Gesualdo',
            'slug': 'mastro-don-gesualdo',
            'anno_pubblicazione': 1889,
            'trama': '''Il romanzo racconta la storia di Gesualdo Motta, un muratore arricchito che 
cerca di elevarsi socialmente sposando una nobildonna decaduta, Bianca Trao. Nonostante la sua 
ricchezza, Gesualdo non viene mai accettato dalla nobiltà e viene disprezzato sia dai nobili che 
dal popolo. La sua vita è segnata dalla solitudine e dall'incomprensione, culminando in una morte 
solitaria e dolorosa, circondato dall'indifferenza di coloro che dovrebbero essergli vicini.''',
            'analisi': '''Secondo romanzo del ciclo dei "Vinti", Mastro-don Gesualdo rappresenta 
l'ascesa sociale impossibile e il tema dell'alienazione. Verga analizza la stratificazione sociale 
siciliana e l'impossibilità di superare le barriere di classe. Il protagonista è vittima delle 
sue stesse ambizioni e della società che lo respinge. L'opera è caratterizzata da una profonda 
analisi psicologica e da un pessimismo esistenziale.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Mastro-don_Gesualdo',
            'copertina_path': 'vizzini/borgo.jpg'
        },
        {
            'titolo': 'Vita dei campi',
            'slug': 'vita-dei-campi',
            'anno_pubblicazione': 1880,
            'trama': '''Raccolta di novelle che descrive la vita contadina siciliana con crudo 
realismo. Tra le novelle più famose vi sono "Rosso Malpelo", storia di un ragazzo dai capelli 
rossi maltrattato e sfruttato, "La Lupa", che narra l'ossessione amorosa di una donna, 
e "Cavalleria rusticana", dramma di gelosia e onore che ispirò la celebre opera lirica di Mascagni.''',
            'analisi': '''Vita dei campi segna l'inizio della stagione verista di Verga. Le novelle 
presentano personaggi umili schiacciati da un destino crudele, vittime delle leggi economiche e 
sociali. Lo stile è essenziale, privo di giudizi morali, con l'autore che si eclissa completamente 
dietro la narrazione. Emerge una visione pessimistica della vita, dove la lotta per la sopravvivenza 
è spietata.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vita_dei_campi_(1880)',
            'copertina_path': 'vizzini/bosco.jpeg'
        },
        {
            'titolo': 'Novelle rusticane',
            'slug': 'novelle-rusticane',
            'anno_pubblicazione': 1883,
            'trama': '''Seconda raccolta di novelle veriste, che continua l'esplorazione del mondo 
contadino siciliano. Include storie come "La roba", che racconta l'ossessione per l'accumulo di 
ricchezze di Mazzarò, "Libertà", una cronaca della rivolta contadina di Bronte del 1860, 
e "Pane nero", storia di miseria e sfruttamento.''',
            'analisi': '''Le Novelle rusticane approfondiscono i temi di Vita dei campi, concentrandosi 
maggiormente sugli aspetti economici della vita rurale. Verga analizza l'ossessione per la proprietà, 
il conflitto tra ricchi e poveri, e le illusioni di riscatto sociale. Lo stile è ancora più 
asciutto e impersonale, con una rappresentazione cruda e oggettiva della realtà.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Novelle_rusticane',
            'copertina_path': 'licodia/panorama.jpg'
        },
        {
            'titolo': 'Eva',
            'slug': 'eva-verga',
            'anno_pubblicazione': 1873,
            'trama': '''Romanzo giovanile che narra la storia d'amore tra Enrico Lanti, un giovane 
siciliano in viaggio per l'Italia, e Eva, una ballerina. Il protagonista si innamora della donna, 
ma il loro amore è destinato a fallire per le differenze sociali e per le convenzioni dell'epoca.''',
            'analisi': '''Eva appartiene ancora al periodo romantico di Verga, prima della sua 
conversione al verismo. L'opera mostra però già alcuni elementi che prefigurano il futuro stile 
dell'autore, come l'attenzione per i dettagli psicologici e la rappresentazione della realtà sociale.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Eva_(Verga)',
            'copertina_path': 'vizzini/casaVerga.jpg'
        },
        {
            'titolo': 'Tigre reale',
            'slug': 'tigre-reale',
            'anno_pubblicazione': 1873,
            'trama': '''Romanzo che narra la storia d'amore tra Giorgio La Ferlita, un giovane siciliano, 
e la contessa russa Natalia, soprannominata "Tigre reale" per il suo carattere indomito. 
L'opera esplora i temi della passione, del tradimento e della morte.''',
            'analisi': '''Anche Tigre reale appartiene al periodo romantico di Verga, ma contiene 
già alcuni spunti che anticipano il verismo, specialmente nella caratterizzazione psicologica 
dei personaggi e nella rappresentazione della società dell'epoca.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Tigre_reale',
            'copertina_path': 'vizzini/duomo.jpg'
        },
        {
            'titolo': 'Storia di una capinera',
            'slug': 'storia-di-una-capinera',
            'anno_pubblicazione': 1871,
            'trama': '''Romanzo epistolare che narra la triste storia di Maria, una giovane che viene 
costretta a prendere i voti. L'opera è scritta in forma di lettere che Maria scrive all'amica Marianna, 
rivelando le sue sofferenze e la sua impossibile storia d'amore.''',
            'analisi': '''Storia di una capinera è uno dei primi successi letterari di Verga e appartiene 
ancora al periodo romantico. L'opera è caratterizzata da un tono sentimentale e melodrammatico, 
molto lontano dal verismo maturo dell'autore.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Storia_di_una_capinera',
            'copertina_path': 'vizzini/duomo_1.jpeg'
        },
        {
            'titolo': 'Per le vie',
            'slug': 'per-le-vie',
            'anno_pubblicazione': 1883,
            'trama': '''Raccolta di novelle ambientate in una Milano in trasformazione, che raccontano 
le vicende di personaggi umili travolti dai cambiamenti sociali ed economici. Le storie mostrano 
la durezza della vita urbana e il contrasto tra tradizione e modernità.''',
            'analisi': '''Per le vie segna un cambiamento di scenario per Verga, che si allontana 
dalla Sicilia per ambientare le sue storie a Milano. L'opera mostra l'applicazione dei principi 
veristi a un contesto urbano e industriale, mantenendo lo stesso stile impersonale e oggettivo.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Per_le_vie',
            'copertina_path': 'vizzini/cunziria.jpg'
        },
        {
            'titolo': 'Vagabondaggio',
            'slug': 'vagabondaggio',
            'anno_pubblicazione': 1887,
            'trama': '''Raccolta di novelle che continua l'esplorazione della vita urbana e delle 
trasformazioni sociali. I personaggi sono emarginati, vagabondi, gente che vive ai margini della 
società, rappresentati con il tipico realismo verista.''',
            'analisi': '''Vagabondaggio approfondisce i temi di Per le vie, concentrandosi maggiormente 
sugli emarginati e sui disadattati. Verga mostra come la modernità non porti necessariamente al 
progresso e alla felicità, ma spesso all'alienazione e alla solitudine.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Vagabondaggio',
            'copertina_path': 'vizzini/comune.jpg'
        },
        {
            'titolo': 'Don Candeloro e C.i',
            'slug': 'don-candeloro-e-ci',
            'anno_pubblicazione': 1894,
            'trama': '''Raccolta di novelle che segna un ritorno parziale al periodo giovanile di Verga, 
con storie più leggere e a volte umoristiche. Il titolo si riferisce a una compagnia teatrale itinerante.''',
            'analisi': '''Don Candeloro e C.i mostra un Verga in parte diverso, più disteso e ironico. 
L'opera dimostra la versatilità dello scrittore, capace di alternare toni tragici e comici, 
mantenendo sempre un alto livello letterario.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Don_Candeloro_e_C.i',
            'copertina_path': 'vizzini/festa.jpeg'
        },
    ]
    
    for opera_data in opere_verga:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': verga,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = verga
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        
        # Copia la copertina se specificata e non esiste già
        if 'copertina_path' in opera_data and not opera.copertina:
            copertina_path = copy_static_to_media(opera_data['copertina_path'], f"copertine_opere/{opera_data['slug']}.jpg")
            if copertina_path:
                media_path = os.path.join(settings.MEDIA_ROOT, copertina_path)
                with open(media_path, 'rb') as f:
                    opera.copertina.save(f"{opera_data['slug']}.jpg", File(f), save=False)
        
        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # OPERE DI LUIGI CAPUANA
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA OPERE DI LUIGI CAPUANA")
    print("="*70)
    
    opere_capuana = [
        {
            'titolo': 'Il marchese di Roccaverdina',
            'slug': 'il-marchese-di-roccaverdina',
            'anno_pubblicazione': 1901,
            'trama': '''Il romanzo narra la storia del marchese di Roccaverdina, che dopo aver 
avuto una lunga relazione con la sua massaia Agrippina Solmo, decide di farla sposare con un 
suo servo, Rocco Criscione, per continuare a frequentarla senza scandalo. Tuttavia, tormentato 
dalla gelosia, il marchese uccide Rocco. Il senso di colpa lo perseguiterà fino alla follia, 
portandolo alla confessione e alla morte.''',
            'analisi': '''Capolavoro di Capuana, il romanzo rappresenta un'evoluzione del verismo 
verso l'analisi psicologica. L'autore esplora i tormenti della coscienza e il conflitto tra 
passione e ragione. La dimensione psicologica prevale su quella sociale, anticipando temi del 
decadentismo. Il marchese è un personaggio complesso, diviso tra il desiderio e il rimorso.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Il_marchese_di_Roccaverdina'
        },
        {
            'titolo': 'Giacinta',
            'slug': 'giacinta',
            'anno_pubblicazione': 1879,
            'trama': '''Giacinta è una giovane donna che, dopo essere stata violentata da bambina, 
sviluppa una personalità disturbata e cerca disperatamente l'amore e l'accettazione. Si sposa 
con Andrea, ma il matrimonio è tormentato dai suoi problemi psicologici. La storia esplora le 
conseguenze del trauma infantile sulla psiche e sulla vita adulta.''',
            'analisi': '''Giacinta è uno dei primi romanzi veristi italiani e uno dei primi a 
trattare apertamente temi come il trauma sessuale e le sue conseguenze psicologiche. Capuana 
utilizza il naturalismo per esplorare l'inconscio e le patologie mentali, anticipando gli 
sviluppi della psicologia moderna. L'opera fu considerata scandalosa per l'epoca.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Giacinta'
        },
        {
            'titolo': 'Profili di donne',
            'slug': 'profili-di-donne',
            'anno_pubblicazione': 1877,
            'trama': '''Raccolta di ritratti femminili che esplorano diversi tipi di donne e le 
loro vicende sentimentali. Capuana analizza con sensibilità psicologica i caratteri femminili, 
le loro passioni, i loro conflitti interiori e il loro rapporto con la società.''',
            'analisi': '''Quest'opera mostra l'interesse di Capuana per la psicologia femminile 
e il suo approccio analitico alla narrazione. I ritratti sono caratterizzati da un'attenzione 
particolare agli stati d'animo e alle motivazioni interiori, prefigurando l'evoluzione verso 
il romanzo psicologico.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Profili_di_donne'
        },
        {
            'titolo': 'Il profumo',
            'slug': 'il-profumo-capuana',
            'anno_pubblicazione': 1890,
            'trama': '''Romanzo che narra la storia di Giovanna, una giovane che si innamora di 
un uomo più anziano. L'opera esplora i temi dell'amore, della gelosia e della passione, con 
una particolare attenzione alla dimensione psicologica dei personaggi.''',
            'analisi': '''Il profumo mostra l'evoluzione stilistica di Capuana verso un romanzo 
più introspettivo e psicologico. L'autore approfondisce l'analisi dei sentimenti e delle 
motivazioni interiori, prefigurando alcune tendenze del romanzo moderno.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Il_profumo'
        },
        {
            'titolo': 'Scurpiddu',
            'slug': 'scurpiddu',
            'anno_pubblicazione': 1888,
            'trama': '''Romanzo che narra la storia di un giovane siciliano, soprannominato 
"Scurpiddu", e delle sue disavventure. L'opera è caratterizzata da un tono più leggero e umoristico, 
che si allontana dal verismo più crudo delle opere precedenti.''',
            'analisi': '''Scurpiddu mostra la versatilità di Capuana, capace di alternare toni 
seri e comici. L'opera dimostra anche l'evoluzione dello scrittore verso uno stile più personale 
e meno legato ai canoni del verismo puro.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Scurpiddu'
        },
        {
            'titolo': 'La Sfinge',
            'slug': 'la-sfinge-capuana',
            'anno_pubblicazione': 1877,
            'trama': '''Romanzo che narra la storia di un uomo che si innamora di una donna misteriosa, 
definita "sfinge" per il suo carattere enigmatico. L'opera esplora i temi dell'amore, della passione 
e dell'ossessione.''',
            'analisi': '''La Sfinge appartiene al periodo giovanile di Capuana, ancora influenzato 
dal romanticismo e dal sentimentalismo. L'opera mostra però già alcuni elementi che prefigurano 
il futuro stile psicologico dell'autore.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/La_Sfinge'
        },
        {
            'titolo': 'Homobonus',
            'slug': 'homobonus',
            'anno_pubblicazione': 1872,
            'trama': '''Romanzo giovanile che narra la storia di un uomo che cerca di vivere secondo 
i principi del bene, nonostante le difficoltà e le tentazioni della vita. L'opera è caratterizzata 
da un tono moraleggiante e didattico.''',
            'analisi': '''Homobonus appartiene al periodo più giovanile di Capuana, quando l'autore 
era ancora influenzato dalle tendenze moraleggianti del romanzo sociale dell'epoca. L'opera è 
lontana dal verismo maturo dello scrittore.''',
            'link_wikisource': 'https://it.wikisource.org/wiki/Homobonus'
        },
    ]
    
    for opera_data in opere_capuana:
        opera, created = Opera.objects.get_or_create(
            slug=opera_data['slug'],
            defaults={
                'autore': capuana,
                'anno_pubblicazione': opera_data['anno_pubblicazione'],
                'link_wikisource': opera_data['link_wikisource']
            }
        )
        if not created:
            opera.autore = capuana
            opera.anno_pubblicazione = opera_data['anno_pubblicazione']
            opera.link_wikisource = opera_data['link_wikisource']
        
        # Copia la copertina se specificata e non esiste già
        if 'copertina_path' in opera_data and not opera.copertina:
            copertina_path = copy_static_to_media(opera_data['copertina_path'], f"copertine_opere/{opera_data['slug']}.jpg")
            if copertina_path:
                media_path = os.path.join(settings.MEDIA_ROOT, copertina_path)
                with open(media_path, 'rb') as f:
                    opera.copertina.save(f"{opera_data['slug']}.jpg", File(f), save=False)
        
        opera.set_current_language('it')
        opera.titolo = opera_data['titolo']
        opera.trama = opera_data['trama']
        opera.analisi = opera_data['analisi']
        opera.save()
        if created:
            print(f"✓ Creata opera: {opera.titolo} ({opera.anno_pubblicazione})")
        else:
            print(f"• Opera aggiornata: {opera.titolo}")
    
    # ========================================================================
    # EVENTI CON FOTO
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA EVENTI CON FOTO")
    print("="*70)
    
    eventi_data = [
        {
            'titolo': 'Presentazione del romanzo "I Malavoglia"',
            'slug': 'presentazione-i-malavoglia',
            'descrizione': '''Il Parco Letterario del Verismo organizza una serata speciale dedicata al capolavoro
di Giovanni Verga. L'evento prevede una lettura guidata dei passi più significativi del romanzo,
seguita da un dibattito con esperti letterari e studiosi del verismo siciliano.

Saranno presenti:
- Letture a cura di attori professionisti
- Analisi critica dell'opera
- Dibattito con il pubblico
- Degustazione di prodotti tipici siciliani

L'evento si terrà nella suggestiva cornice di Aci Trezza, luogo natale del romanzo.''',
            'data_inizio': datetime(2025, 12, 15, 18, 30),
            'data_fine': datetime(2025, 12, 15, 22, 00),
            'luogo': 'Aci Trezza - Teatro Comunale',
            'indirizzo': 'Via Teatro, 1 - 95021 Aci Trezza (CT)',
            'immagine_path': 'vizzini/casaVerga.jpg',
            'is_active': True
        },
        {
            'titolo': 'Visita guidata ai luoghi verghiani',
            'slug': 'visita-guidata-luoghi-verghiani',
            'descrizione': '''Scopri i luoghi che hanno ispirato le opere di Giovanni Verga in una visita guidata
esclusiva organizzata dal Parco Letterario del Verismo.

Il percorso toccherà:
- La casa di Giovanni Verga a Vizzini
- I luoghi di "I Malavoglia" ad Aci Trezza
- I paesaggi che hanno ispirato "Vita dei campi"
- Le chiese e i monumenti storici menzionati nelle opere

La visita è gratuita e dura circa 3 ore. Prenotazione obbligatoria.''',
            'data_inizio': datetime(2025, 11, 20, 9, 00),
            'data_fine': datetime(2025, 11, 20, 12, 00),
            'luogo': 'Vizzini - Casa di Giovanni Verga',
            'indirizzo': 'Via Giovanni Verga - 95049 Vizzini (CT)',
            'immagine_path': 'vizzini/centrostorico.jpg',
            'is_active': True
        },
        {
            'titolo': 'Visita guidata alla casa di Luigi Capuana',
            'slug': 'visita-casa-capuana',
            'descrizione': '''Visita esclusiva alla casa natale di Luigi Capuana a Mineo, uno dei luoghi più 
significativi del Parco Letterario del Verismo.

Durante la visita potrete:
- Visitare le stanze dove visse Capuana
- Ammirare i manoscritti e i documenti originali
- Scoprire la biblioteca personale dello scrittore
- Conoscere la storia e le tradizioni di Mineo

La visita è guidata da esperti del Parco Letterario.''',
            'data_inizio': datetime(2025, 11, 25, 10, 00),
            'data_fine': datetime(2025, 11, 25, 12, 30),
            'luogo': 'Mineo - Casa Museo Luigi Capuana',
            'indirizzo': 'Via Luigi Capuana - 95044 Mineo (CT)',
            'immagine_path': 'mineo/Casa-Luigi-Capuana.jpg',
            'is_active': True
        },
        {
            'titolo': 'Festival del Verismo Siciliano',
            'slug': 'festival-verismo-siciliano',
            'descrizione': '''Il Festival del Verismo Siciliano è un evento annuale che celebra la letteratura 
verista e la cultura siciliana attraverso spettacoli, conferenze e laboratori.

Il festival prevede:
- Spettacoli teatrali tratti dalle opere di Verga e Capuana
- Conferenze con critici letterari e studiosi
- Laboratori di scrittura creativa
- Mostre fotografiche sui luoghi verghiani
- Degustazioni di prodotti tipici siciliani

L'evento si svolge nei comuni del Parco Letterario del Verismo.''',
            'data_inizio': datetime(2026, 3, 15, 10, 00),
            'data_fine': datetime(2026, 3, 17, 22, 00),
            'luogo': 'Vizzini, Mineo e Licodia Eubea',
            'indirizzo': 'Vari comuni del Parco Letterario',
            'immagine_path': 'vizzini/festa.jpeg',
            'is_active': True
        },
        {
            'titolo': 'Convegno: Il Verismo oggi',
            'slug': 'convegno-verismo-oggi',
            'descrizione': '''Un convegno internazionale dedicato all'attualità del verismo nella letteratura
contemporanea. Interverranno critici letterari, scrittori e accademici da tutta Italia.

Temi trattati:
- L'eredità del verismo nella narrativa italiana contemporanea
- Verga e Capuana: maestri del realismo
- Il verismo siciliano e la letteratura europea
- Nuove prospettive critiche sul movimento verista

L'evento è accreditato per la formazione docenti.''',
            'data_inizio': datetime(2026, 1, 25, 9, 30),
            'data_fine': datetime(2026, 1, 25, 18, 00),
            'luogo': 'Università di Catania - Aula Magna',
            'indirizzo': 'Via Biblioteca, 4 - 95124 Catania',
            'immagine_path': 'vizzini/duomo.jpg',
            'is_active': True
        },
    ]
    
    for evento_data in eventi_data:
        evento, created = Evento.objects.get_or_create(
            slug=evento_data['slug'],
            defaults={
                'data_inizio': evento_data['data_inizio'],
                'data_fine': evento_data.get('data_fine'),
                'is_active': evento_data.get('is_active', True)
            }
        )
        if not created:
            evento.data_inizio = evento_data['data_inizio']
            evento.data_fine = evento_data.get('data_fine')
            evento.is_active = evento_data.get('is_active', True)
        
        # Copia l'immagine se specificata
        if 'immagine_path' in evento_data and not evento.immagine:
            image_path = copy_static_to_media(evento_data['immagine_path'], f"eventi/{evento_data['slug']}.jpg")
            if image_path:
                media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(media_path, 'rb') as f:
                    evento.immagine.save(f"{evento_data['slug']}.jpg", File(f), save=False)
        
        evento.set_current_language('it')
        evento.titolo = evento_data['titolo']
        evento.descrizione = evento_data['descrizione']
        evento.luogo = evento_data['luogo']
        evento.indirizzo = evento_data.get('indirizzo', '')
        evento.save()
        if created:
            print(f"✓ Creato evento: {evento.titolo} ({evento.data_inizio.date()})")
        else:
            print(f"• Evento aggiornato: {evento.titolo}")
    
    # ========================================================================
    # NOTIZIE CON FOTO
    # ========================================================================
    print("\n" + "="*70)
    print("AGGIUNTA NOTIZIE CON FOTO")
    print("="*70)
    
    notizie_data = [
        {
            'titolo': 'Il Parco Letterario del Verismo ottiene il riconoscimento UNESCO',
            'slug': 'riconoscimento-unesco',
            'contenuto': '''Siamo orgogliosi di annunciare che il Parco Letterario del Verismo è stato ufficialmente
riconosciuto come Patrimonio Culturale Immateriale dell'Umanità dall'UNESCO.

Questo importante riconoscimento premia il lavoro svolto negli ultimi anni per la valorizzazione
del patrimonio letterario verista e la promozione della cultura siciliana nel mondo.

Il riconoscimento UNESCO rappresenta un importante passo avanti per la tutela e la promozione
del nostro patrimonio culturale, e ci impegna a continuare il nostro lavoro con ancora maggiore
dedizione e professionalità.

Ringraziamo tutti i partner, le istituzioni e i cittadini che hanno sostenuto questo progetto.''',
            'riassunto': 'Il Parco Letterario del Verismo ottiene il prestigioso riconoscimento UNESCO come Patrimonio Culturale Immateriale.',
            'immagine_path': 'vizzini/comune.jpg',
            'is_active': True
        },
        {
            'titolo': 'Nuova pubblicazione: Guida ai luoghi verghiani',
            'slug': 'guida-luoghi-verghiani',
            'contenuto': '''È disponibile la nuova guida "Alla scoperta dei luoghi verghiani", una pubblicazione
bilingue (italiano-inglese) che accompagna i visitatori alla scoperta dei luoghi che hanno ispirato
le opere di Giovanni Verga.

La guida, realizzata in collaborazione con l'Università di Catania, contiene:
- Mappe dettagliate dei percorsi letterari
- Descrizioni storiche e letterarie dei luoghi
- Fotografie d'epoca e moderne
- Citazioni dalle opere di Verga
- Informazioni pratiche per i visitatori

La pubblicazione è disponibile gratuitamente presso gli uffici del Parco e sul nostro sito web.''',
            'riassunto': 'Disponibile la nuova guida bilingue per scoprire i luoghi che hanno ispirato le opere di Giovanni Verga.',
            'immagine_path': 'vizzini/borgo.jpg',
            'is_active': True
        },
        {
            'titolo': 'Progetto educativo: Il verismo a scuola',
            'slug': 'progetto-educativo-verismo',
            'contenuto': '''Il Parco Letterario del Verismo ha avviato un nuovo progetto educativo rivolto
agli studenti delle scuole superiori siciliane.

Il progetto "Il verismo a scuola" prevede:
- Visite guidate gratuite per le classi
- Laboratori di scrittura creativa ispirati al verismo
- Incontri con scrittori e critici letterari
- Concorso letterario per studenti
- Materiali didattici digitali

L'iniziativa coinvolgerà oltre 50 istituti scolastici e mira a far conoscere il movimento
verista alle nuove generazioni, stimolando l'interesse per la letteratura e la cultura siciliana.

Le scuole interessate possono contattare gli uffici del Parco per informazioni e prenotazioni.''',
            'riassunto': 'Nuovo progetto educativo per portare il verismo nelle scuole siciliane con visite guidate e laboratori.',
            'immagine_path': 'mineo/premio-luigi.jpg',
            'is_active': True
        },
        {
            'titolo': 'Restauro della casa di Giovanni Verga a Vizzini',
            'slug': 'restauro-casa-verga',
            'contenuto': '''È stato completato il restauro della casa natale di Giovanni Verga a Vizzini. 
Il restauro ha interessato sia la struttura esterna che gli interni, riportando l'edificio 
all'antico splendore.

La casa, ora museo, sarà aperta al pubblico a partire dal prossimo mese e ospiterà:
- Mostre permanenti sulla vita e le opere di Verga
- Biblioteca specializzata sul verismo
- Archivio documenti e manoscritti
- Spazi per eventi e conferenze

Il restauro è stato possibile grazie al contributo della Regione Siciliana e dell'Unione Europea.''',
            'riassunto': 'Completato il restauro della casa natale di Giovanni Verga a Vizzini, che diventerà un museo aperto al pubblico.',
            'immagine_path': 'vizzini/casaVerga.jpg',
            'is_active': True
        },
        {
            'titolo': 'Settimana Santa a Licodia Eubea: tradizioni e letteratura',
            'slug': 'settimana-santa-licodia',
            'contenuto': '''Il Parco Letterario del Verismo partecipa alle celebrazioni della Settimana Santa a Licodia Eubea,
un evento che unisce tradizione religiosa e cultura letteraria.

Durante la Settimana Santa si terranno:
- Processioni storiche per le vie del paese
- Letture pubbliche di brani tratti dalle opere veriste
- Visite guidate ai luoghi storici
- Mostre fotografiche sulle tradizioni locali

L'evento rappresenta un'occasione unica per scoprire come le tradizioni siciliane siano state 
raccontate dai grandi autori del verismo.''',
            'riassunto': 'Il Parco Letterario partecipa alle celebrazioni della Settimana Santa a Licodia Eubea, unendo tradizione e letteratura.',
            'immagine_path': 'licodia/settimana_santa.jpg',
            'is_active': True
        },
    ]
    
    for notizia_data in notizie_data:
        notizia, created = Notizia.objects.get_or_create(
            slug=notizia_data['slug'],
            defaults={
                'is_active': notizia_data.get('is_active', True)
            }
        )
        if not created:
            notizia.is_active = notizia_data.get('is_active', True)
        
        # Copia l'immagine se specificata
        if 'immagine_path' in notizia_data and not notizia.immagine:
            image_path = copy_static_to_media(notizia_data['immagine_path'], f"notizie/{notizia_data['slug']}.jpg")
            if image_path:
                media_path = os.path.join(settings.MEDIA_ROOT, image_path)
                with open(media_path, 'rb') as f:
                    notizia.immagine.save(f"{notizia_data['slug']}.jpg", File(f), save=False)
        
        notizia.set_current_language('it')
        notizia.titolo = notizia_data['titolo']
        notizia.contenuto = notizia_data['contenuto']
        notizia.riassunto = notizia_data['riassunto']
        notizia.save()
        if created:
            print(f"✓ Creata notizia: {notizia.titolo}")
        else:
            print(f"• Notizia aggiornata: {notizia.titolo}")
    
    # ========================================================================
    # ARCHIVIO FOTOGRAFICO
    # ========================================================================
    print("\n" + "="*70)
    print("POPOLAMENTO ARCHIVIO FOTOGRAFICO")
    print("="*70)
    
    # Foto di Vizzini
    foto_vizzini = [
        ('vizzini/casaVerga.jpg', 'Casa di Giovanni Verga', 'La casa natale di Giovanni Verga a Vizzini, oggi museo dedicato allo scrittore.', 'Luoghi'),
        ('vizzini/centrostorico.jpg', 'Centro Storico di Vizzini', 'Il suggestivo centro storico di Vizzini con le sue caratteristiche vie.', 'Luoghi'),
        ('vizzini/duomo.jpg', 'Duomo di Vizzini', 'Il Duomo di Vizzini, uno dei principali monumenti storici della città.', 'Luoghi'),
        ('vizzini/borgo.jpg', 'Borgo di Vizzini', 'Il caratteristico borgo di Vizzini che ha ispirato molte opere di Verga.', 'Luoghi'),
        ('vizzini/cunziria.jpg', 'La Cunziria', 'L\'antica conceria di Vizzini, luogo caratteristico del paese.', 'Luoghi'),
        ('vizzini/festa.jpeg', 'Festa a Vizzini', 'Una festa tradizionale a Vizzini durante le celebrazioni estive.', 'Eventi'),
        ('vizzini/festaRicotta.jpg', 'Festa della Ricotta', 'La tradizionale festa della ricotta di Vizzini.', 'Eventi'),
        ('vizzini/processione.jpg', 'Processione religiosa', 'Una processione religiosa per le vie di Vizzini.', 'Eventi'),
        ('vizzini/verga.jpeg', 'Giovanni Verga', 'Ritratto di Giovanni Verga, il grande scrittore verista.', 'Personaggi'),
        ('vizzini/bosco.jpeg', 'Bosco di Vizzini', 'Il paesaggio naturale intorno a Vizzini.', 'Luoghi'),
    ]
    
    # Foto di Mineo
    foto_mineo = [
        ('mineo/Casa-Luigi-Capuana.jpg', 'Casa di Luigi Capuana', 'La casa natale di Luigi Capuana a Mineo.', 'Luoghi'),
        ('mineo/centro-storico.jpg', 'Centro Storico di Mineo', 'Il centro storico di Mineo con i suoi vicoli caratteristici.', 'Luoghi'),
        ('mineo/castello.jpg', 'Castello di Mineo', 'L\'antico castello di Mineo, simbolo della città.', 'Luoghi'),
        ('mineo/panorama.jpg', 'Panorama di Mineo', 'Il suggestivo panorama dai colli di Mineo.', 'Luoghi'),
        ('mineo/chiesa.jpg', 'Chiesa di Mineo', 'Una delle chiese storiche di Mineo.', 'Luoghi'),
        ('mineo/premio-luigi.jpg', 'Premio Luigi Capuana', 'La cerimonia del Premio letterario intitolato a Luigi Capuana.', 'Eventi'),
        ('mineo/santa-agrippina.jpg', 'Chiesa di Santa Agrippina', 'La chiesa dedicata a Santa Agrippina, patrona di Mineo.', 'Luoghi'),
    ]
    
    # Foto di Licodia Eubea
    foto_licodia = [
        ('licodia/hero-bg.jpg', 'Licodia Eubea', 'Veduta panoramica di Licodia Eubea.', 'Luoghi'),
        ('licodia/chiesa_santa_margherita.jpg', 'Chiesa di Santa Margherita', 'La chiesa di Santa Margherita a Licodia Eubea.', 'Luoghi'),
        ('licodia/colle_castello.jpg', 'Colle del Castello', 'Il colle del castello di Licodia Eubea.', 'Luoghi'),
        ('licodia/panorama.jpg', 'Panorama di Licodia', 'Il suggestivo panorama dai colli di Licodia Eubea.', 'Luoghi'),
        ('licodia/settimana_santa.jpg', 'Settimana Santa', 'Le celebrazioni della Settimana Santa a Licodia Eubea.', 'Eventi'),
        ('licodia/festa_dell_uva.jpeg', 'Festa dell\'Uva', 'La tradizionale festa dell\'uva a Licodia Eubea.', 'Eventi'),
        ('licodia/sagra.jpg', 'Sagra locale', 'Una sagra tradizionale a Licodia Eubea.', 'Eventi'),
    ]
    
    ordine = 0
    tutte_le_foto = [
        ('Vizzini', foto_vizzini),
        ('Mineo', foto_mineo),
        ('Licodia Eubea', foto_licodia),
    ]
    
    for comune, foto_list in tutte_le_foto:
        for immagine_path, titolo, descrizione, categoria in foto_list:
            # Controlla se la foto esiste già
            static_path = os.path.join(settings.BASE_DIR, 'parco_verismo', 'static', 'assets', 'img', immagine_path)
            if not os.path.exists(static_path):
                print(f"⚠ Immagine non trovata: {immagine_path}")
                continue
            
            # Crea il nome unico per la foto
            foto_slug = os.path.splitext(os.path.basename(immagine_path))[0]
            foto_id = f"{comune.lower()}_{foto_slug}"
            
            # Verifica se la foto esiste già nel database basandosi sul titolo
            foto = FotoArchivio.objects.filter(translations__titolo=titolo).first()
            if not foto:
                foto = FotoArchivio()
                created = True
            else:
                created = False
            
            if not foto.immagine:
                # Copia l'immagine
                image_path_rel = copy_static_to_media(immagine_path, f"archivio_fotografico/{comune.lower()}_{foto_slug}.jpg")
                if image_path_rel:
                    media_path = os.path.join(settings.MEDIA_ROOT, image_path_rel)
                    with open(media_path, 'rb') as f:
                        foto.immagine.save(f"{foto_slug}.jpg", File(f), save=False)
            
            foto.ordine = ordine
            foto.categoria = categoria
            foto.is_active = True
            foto.set_current_language('it')
            foto.titolo = titolo
            foto.descrizione = descrizione
            foto.save()
            
            if created:
                print(f"✓ Aggiunta foto: {foto.titolo} ({comune})")
            else:
                print(f"• Foto aggiornata: {foto.titolo}")
            
            ordine += 1
    
    # ========================================================================
    # RIEPILOGO FINALE
    # ========================================================================
    print("\n" + "="*70)
    print("POPOLAMENTO COMPLETATO CON SUCCESSO!")
    print("="*70)
    print(f"\nTotale autori: {Autore.objects.count()}")
    print(f"Totale opere: {Opera.objects.count()}")
    print(f"  - Opere di Verga: {Opera.objects.filter(autore=verga).count()}")
    print(f"  - Opere di Capuana: {Opera.objects.filter(autore=capuana).count()}")
    print(f"Totale eventi: {Evento.objects.count()}")
    print(f"Totale notizie: {Notizia.objects.count()}")
    print(f"Totale foto archivio: {FotoArchivio.objects.count()}")
    print(f"\nPuoi ora avviare il server con:")
    print("  python manage.py runserver")
    print("\nE visitare:")
    print("  - Biblioteca: http://127.0.0.1:8000/biblioteca/")
    print("  - Eventi: http://127.0.0.1:8000/eventi/")
    print("  - Calendario: http://127.0.0.1:8000/calendario/")
    print("  - Notizie: http://127.0.0.1:8000/notizie/")
    print("  - Archivio Fotografico: http://127.0.0.1:8000/archivio/")

if __name__ == '__main__':
    populate()


import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

def optimize_image(image_field, max_width=1920, quality=85):
    """
    Ottimizza un'immagine: la converte in WebP e applica una compressione 
    mantenendo un'alta qualità.
    Ridimensiona l'immagine (max_width) MANTENENDO LE PROPORZIONI (aspect ratio).
    """
    if not image_field:
        return

    # Apri l'immagine con PIL
    img = Image.open(image_field)
    
    # Se l'immagine è già in WebP e non supera la larghezza massima, 
    # potremmo saltare l'ottimizzazione, ma per semplicità la ri-elaboriamo
    # per garantire la compressione impostata.

    # Converti in RGB se necessario (WebP supporta RGBA, ma se vogliamo 
    # forzare RGB per risparmiare ulteriore spazio possiamo farlo. 
    # Qui manteniamo RGBA se presente per i loghi/trasparenze).
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGBA")
    else:
        img = img.convert("RGB")

    # Ridimensionamento proporzionale (ASPECT RATIO PRESERVATO)
    if max_width and img.width > max_width:
        ratio = max_width / float(img.width)
        new_height = int(float(img.height) * float(ratio))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

    # Salva in un buffer in memoria come WebP
    output = BytesIO()
    img.save(output, format="WEBP", quality=quality, method=6) # method 6 is slowest/best compression
    output.seek(0)

    # Prepara il nuovo nome file (cambia estensione in .webp)
    filename = os.path.splitext(image_field.name)[0] + ".webp"

    # Sostituisci il file nel campo del modello
    new_image = InMemoryUploadedFile(
        output,
        'ImageField',
        filename,
        'image/webp',
        output.getbuffer().nbytes,
        None
    )
    
    return new_image

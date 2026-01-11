"""
Admin per Eventi e Notizie.
"""

# Django imports
from django.contrib import admin

# Third-party imports
from parler.admin import TranslatableAdmin

# Local imports
from ..models import Evento, Notizia, EventoImage, NotiziaImage
from django import forms
from parler.forms import TranslatableModelForm


class EventoImageInline(admin.TabularInline):
    model = EventoImage
    extra = 1


class NotiziaImageInline(admin.TabularInline):
    model = NotiziaImage
    extra = 1


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class EventoForm(TranslatableModelForm):
    nuove_foto_galleria = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        help_text="Seleziona più foto da aggiungere alla galleria."
    )
    class Meta:
        model = Evento
        fields = '__all__'


class NotiziaForm(TranslatableModelForm):
    nuove_foto_galleria = forms.FileField(
        widget=MultipleFileInput(attrs={'multiple': True}),
        required=False,
        help_text="Seleziona più foto da aggiungere alla galleria."
    )
    class Meta:
        model = Notizia
        fields = '__all__'


@admin.register(Evento)
class EventoAdmin(TranslatableAdmin):
    form = EventoForm
    list_display = ("__str__", "data_inizio", "data_fine", "is_active")
    list_filter = ("is_active", "data_inizio")
    search_fields = ("translations__titolo", "translations__luogo")
    date_hierarchy = "data_inizio"
    ordering = ("-data_inizio",)
    list_editable = ("is_active",)
    inlines = [EventoImageInline]
    
    # get_form rimosso perché usiamo form = EventoForm explicit definition

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = request.FILES.getlist('nuove_foto_galleria')
        for f in files:
            EventoImage.objects.create(evento=obj, immagine=f)


@admin.register(Notizia)
class NotiziaAdmin(TranslatableAdmin):
    form = NotiziaForm
    list_display = ("__str__", "data_pubblicazione", "is_active")
    list_filter = ("is_active", "data_pubblicazione")
    search_fields = ("translations__titolo", "translations__contenuto")
    date_hierarchy = "data_pubblicazione"
    ordering = ("-data_pubblicazione",)
    list_editable = ("is_active",)
    inlines = [NotiziaImageInline]



    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        files = request.FILES.getlist('nuove_foto_galleria')
        for f in files:
            NotiziaImage.objects.create(notizia=obj, immagine=f)

from django.contrib import admin
from django import forms
from .models import Event, Game, Log, Image, MotionRepresentation, CognitionRepresentation, Annotation

class AnnotationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].queryset = Image.objects.none()

    class Meta:
        model = Annotation
        fields = '__all__'

    def clean_image(self):
        image_id = self.cleaned_data.get('image')
        if image_id:
            return Image.objects.get(id=image_id)
        return None

class ImageAdmin(admin.ModelAdmin):
    search_fields = ['log__log_path','image_url__icontains']
    list_display = ["log","frame_number"]

class LogAdmin(admin.ModelAdmin):
    search_fields = ['log_path__icontains']

class AnnotationAdmin(admin.ModelAdmin):
    raw_id_fields = ('image',)
    list_per_page = 50

class CognitionRepresentationAdmin(admin.ModelAdmin):
    search_fields = ['frame_number__icontains', 'representation_name__icontains']
    list_display = ["log_id","frame_number", 'representation_name']
    list_per_page = 5000

# Register your models here.
admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Log, LogAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(CognitionRepresentation, CognitionRepresentationAdmin)
admin.site.register(MotionRepresentation)
admin.site.register(Annotation, AnnotationAdmin)

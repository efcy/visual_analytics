from django.contrib import admin
from .models import Annotation


# Register your models here.
class AnnotationAdmin(admin.ModelAdmin):
    raw_id_fields = ("image",)
    list_per_page = 50


admin.site.register(Annotation, AnnotationAdmin)

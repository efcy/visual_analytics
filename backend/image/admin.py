
from django.contrib import admin
from .models import Image


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    search_fields = ['log_id__log_path','image_url__icontains']
    list_display = ["log_id","frame_number"]


admin.site.register(Image, ImageAdmin)

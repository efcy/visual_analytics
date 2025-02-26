from django.contrib import admin
from .models import NaoImage


# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    search_fields = ["frame__log_log_path", "image_url__icontains"]
    list_display = ["frame"]


admin.site.register(NaoImage, ImageAdmin)

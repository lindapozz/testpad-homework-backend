from django.contrib import admin

from .models import Url

class UrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'result')

# Register your models here.

admin.site.register(Url, UrlAdmin)
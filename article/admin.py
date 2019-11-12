from django.contrib import admin
from .models import Content

# Register your models here.

class ContentAdmin(admin.ModelAdmin):

    list_per_page = 10

admin.site.register(Content, ContentAdmin)

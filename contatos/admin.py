from django.contrib import admin
from .models import Contato

class ContatoAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'data_nascimento', 'senha')
    list_display_links = ('id', )
    list_per_page: 10

admin.site.register(Contato, ContatoAdmin)

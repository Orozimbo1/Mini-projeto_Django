from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('busca/', views.busca, name='busca'),
    path('json/', views.contatos_json, name='json'),
    path('cvs/', views.contatos_cvs, name='cvs'),
    path('xlxs/', views.contatos_xlxs, name='xlxs'),
    path('<int:contato_id>', views.ver_contato, name='ver_contato'),
]
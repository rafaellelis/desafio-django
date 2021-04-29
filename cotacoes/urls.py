from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:titulo_id>/titulo/', views.detalhaTitulo, name='detalhaTitulo'),
    path('listaTitulos/', views.listaTitulos, name='listaTitulos')
]

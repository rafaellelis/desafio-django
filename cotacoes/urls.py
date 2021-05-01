from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/titulo/', views.DetalharTituloView.as_view(), name='detalhaTitulo'),
    path('configuracao/new/<int:titulo_id>', views.configuracao_new, name='configuracao_new'),
]

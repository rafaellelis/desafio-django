from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/titulo/', views.DetalharTituloView.as_view(), name='detalhaTitulo'),
    path('configuracao/new/<int:titulo_id>', views.configuracao_new, name='configuracao_new'),
    path('configuracao/inativar/<int:titulo_id>', views.configuracao_inativar, name='configuracao_inativar'),
    path('configuracao/reativar/<int:titulo_id>', views.configuracao_reativar, name='configuracao_reativar'),
    path('configuracao/remover/<int:titulo_id>', views.configuracao_remover, name='configuracao_remover'),
]

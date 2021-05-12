from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('', views.titulo_all, name='index'),
    path('<int:titulo_id>/titulo/', views.titulo_detail, name='detalhaTitulo'),
    path('configuracao/new/<int:titulo_id>', views.configuracao_new, name='configuracao_new'),
    path('configuracao/edit/<int:titulo_id>', views.configuracao_editar, name='configuracao_editar'),
    path('configuracao/inativar/<int:titulo_id>', views.configuracao_inativar, name='configuracao_inativar'),
    path('configuracao/reativar/<int:titulo_id>', views.configuracao_reativar, name='configuracao_reativar'),
    path('configuracao/remover/<int:titulo_id>', views.configuracao_remover, name='configuracao_remover'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/titulo/', views.DetalharTituloView.as_view(), name='detalhaTitulo'),
    path('<int:pk>/monitorar/', views.MonitorarTituloView.as_view(), name='monitorarTitulo'),
]

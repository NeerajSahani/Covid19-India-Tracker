from django.urls import path
from . import views

app_name = 'covid19'

urlpatterns = [
    path('', views.index, name='index'),
    path('map/', views.plot_map, name='map'),
    path('hits/', views.get_hits, name='hits'),
]

from django.urls import path
from . import views

app_name = 'scro'

urlpatterns = [
    path('', views.game, name='game'),
]
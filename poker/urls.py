from django.urls import path
from . import views

app_name = 'poker'

urlpatterns = [
    path('', views.index, name='index'),
    path('bet/', views.place_bet, name='place_bet'),
    path('exchange/', views.exchange_cards, name='exchange_cards'),
    path('rankings/', views.hand_ranking, name='hand_ranking'),
    path('gameover/', views.game_over, name='game_over'),
    path('reset/', views.reset_game, name='reset_game'),
]
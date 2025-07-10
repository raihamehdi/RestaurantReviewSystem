
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('review/', views.review, name='review'),
    path('api/review/', views.add_review, name='add_review'),
    path('api/leaderboard/', views.get_leaderboard, name='get_leaderboard'),
    path('api/restaurant/', views.add_restaurant, name='add_restaurant'),
]

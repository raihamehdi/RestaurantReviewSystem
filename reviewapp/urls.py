from django.urls import path
from . import views

urlpatterns = [
    path('review/', views.add_review),
    path('leaderboard/', views.leaderboard),
]

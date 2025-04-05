from core.views.leaderboard_view import ScoreView
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('score', ScoreView.as_view(), name='score'),
]
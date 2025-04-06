from core.views.leaderboard_view import ScoreView, LeaderboardView, RankView
from django.urls import path

app_name = 'core'

urlpatterns = [
    path('score', ScoreView.as_view(), name='score'),
    path('top', LeaderboardView.as_view(), name='leaderboard'),
    path('rank/<int:user_id>', RankView.as_view(), name='rank'),
]
from core.models.user import User
from core.models.leaderboard import Leaderboard
from core.models.game_session import GameSession
from core.tasks.leaderboard import update_leaderboard_task
from django.db import transaction, models
from datetime import datetime
from celery import shared_task

class LeaderBoardService:
    def __init__(self):
        pass

    def submit_score(self, user_id, score):
        with transaction.atomic():
            game_session = GameSession.objects.create(
                user_id=user_id,
                score = score
            )

            # Trigger leaderboard update as a background task
            update_leaderboard_task.delay(user_id)

    def get_rank(self, user_id):
        user_on_leaderboard =  Leaderboard.objects.filter(
            user_id=user_id,
            is_deleted=False,
        ).first()
    
        if user_on_leaderboard:
            return user_on_leaderboard.rank
        else:
            return None

    def get_leaderboard(self, limit=10):
        leaderboard_entries = Leaderboard.objects.filter(
            is_deleted=False,
        ).order_by('rank')[:limit]

        leaderboard_data = []
        for entry in leaderboard_entries:
            user = User.objects.get(id=entry.user_id)
            leaderboard_data.append({
                'user_id': entry.user_id,
                'username': user.username,
                'score': entry.score,
                'rank': entry.rank,
            })

        return leaderboard_data
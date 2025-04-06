from celery import shared_task
from core.models.game_session import GameSession
from core.models.leaderboard import Leaderboard
from django.db import transaction
from django.db.models import Sum

BATCH_SIZE = 1000

@shared_task
def update_leaderboard_task(user_id):
    """
        Updates leaderboard for all the users whose rank can be affected in batch of 1000.
        Optimization: This can be optimized further by only updating ranking of first 1000 affected users, instead of all users. This will
        improves runtime of the task but ranks will be eventually consistent.
    """
    with transaction.atomic():
        total_score = (
            GameSession.objects
            .filter(user_id=user_id)
            .aggregate(score=Sum('score'))['score'] or 0
        )

        user_entry, _ = Leaderboard.objects.get_or_create(
            user_id=user_id,
            defaults={'score': total_score, 'rank': 0, 'is_deleted': False}
        )
        old_score = user_entry.score
        user_entry.score = total_score
        user_entry.is_deleted = False
        user_entry.deleted_at = None
        user_entry.save()

        # Manual pagination over affected leaderboard entries
        current_rank = 1
        last_score = None
        actual_rank = 1
        batch_index = 0

        while True:
            batch_qs = (
                Leaderboard.objects
                .filter(
                    is_deleted=False,
                    score__gte=old_score
                )
                .order_by('-score', 'user_id')
                .select_for_update(skip_locked=True)[batch_index * BATCH_SIZE:(batch_index + 1) * BATCH_SIZE]
            )

            batch = list(batch_qs)
            if not batch:
                break

            if batch_index == 1:
                break

            for entry in batch:
                if last_score is None or entry.score != last_score:
                    current_rank = actual_rank
                    last_score = entry.score
                entry.rank = current_rank
                actual_rank += 1

            Leaderboard.objects.bulk_update(batch, ['rank'])
            batch_index += 1

from celery import shared_task
from core.models.game_session import GameSession
from core.models.leaderboard import Leaderboard
from django.db import transaction, models
from datetime import datetime

@shared_task
def update_leaderboard_task():
    with transaction.atomic():
        aggregated_scores = (
            GameSession.objects
            .values('user_id')
            .annotate(total_score=models.Sum('score'))
            .order_by('-total_score')
        )

        user_score_rank_map = {
            entry['user_id']: {'score': entry['total_score'], 'rank': rank}
            for rank, entry in enumerate(aggregated_scores, start=1)
        }

        existing_entries = list(Leaderboard.objects.select_for_update().filter(is_deleted=False))
        existing_user_ids = {entry.user_id for entry in existing_entries}

        # Update existing entries
        for entry in existing_entries:
            update = user_score_rank_map.get(entry.user_id)
            if update:
                entry.score = update['score']
                entry.rank = update['rank']
            else:
                entry.is_deleted = True
                entry.deleted_at = datetime.now()

        # Create new leaderboard entries
        new_entries = []
        for user_id, data in user_score_rank_map.items():
            if user_id not in existing_user_ids:
                new_entries.append(
                    Leaderboard(
                        user_id=user_id,
                        score=data['score'],
                        rank=data['rank']
                    )
                )

        if new_entries:
            Leaderboard.objects.bulk_create(new_entries)

        Leaderboard.objects.bulk_update(
            existing_entries,
            ['score', 'rank', 'is_deleted', 'deleted_at']
        )

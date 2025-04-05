from core.models.user import User
from core.models.leaderboard import Leaderboard
from core.models.game_session import GameSession
from django.db import transaction, models
from datetime import datetime

class LeaderBoardService:
    def __init__(self):
        pass

    def __update_leaderboard(self, all_entries):
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

        for entry in all_entries:
            update = user_score_rank_map.get(entry.user_id)
            if update:
                entry.score = update['score']
                entry.rank = update['rank']
            else:
                # This user no longer has game sessions — delete their leaderboard entry
                entry.is_deleted = True
                entry.deleted_at = datetime.now()

        Leaderboard.objects.bulk_update(all_entries, ['score', 'rank', 'is_deleted', 'deleted_at'])

    def submit_score(self, user_id, score):
        with transaction.atomic():
            game_session = GameSession.objects.create(
                user_id=user_id,
                score = score
            )

            # Lock leaderboard entries for safe concurrent updates
            all_leaderboard_entries = list(
                Leaderboard.objects.select_for_update().filter(is_deleted=False)
            )

            user_entry = next((entry for entry in all_leaderboard_entries if entry.user_id == user_id), None)

            if not user_entry:
                # give it max rank
                max_rank = max((entry.rank for entry in all_leaderboard_entries), default=0)
                user_entry = Leaderboard(
                    user_id=user_id,
                    score=score,
                    rank=max_rank + 1
                )
                user_entry.save()
                all_leaderboard_entries.append(user_entry)

            self.__update_leaderboard(all_entries=all_leaderboard_entries)
            return True

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
        pass
from django.db import models
from core.models.base import BaseModel
from core.models.user import User

class Leaderboard(BaseModel):
    class Meta:
        db_table = "leaderboards"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leaderboards"
    )

    score = models.IntegerField(db_index=True)
    rank = models.PositiveBigIntegerField(db_index=True)
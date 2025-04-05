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

    score = models.IntegerField()
    rank = models.PositiveBigIntegerField()
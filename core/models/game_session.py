from django.db import models
from core.models.base import BaseModel
from core.models.user import User

class GameSession(BaseModel):
    class Meta:
        db_table = "game_sessions"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="game_sessions"
    )

    score = models.IntegerField()
    game_mode = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

from django.db import models
from core.models.base import BaseModel

class User(BaseModel):
    class Meta:
        db_table = "users"
    
    username = models.CharField(max_length=255, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
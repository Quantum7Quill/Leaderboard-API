from rest_framework import serializers
from core.models import User, GameSession, Leaderboard

class ScoreSerializer(serializers.Serializer):
    score = serializers.IntegerField()
    user_id = serializers.IntegerField()

    def validate(self, attrs):
        user_id = attrs.get('user_id')
        score = attrs.get('score')

        if not User.objects.filter(id=user_id, is_deleted=False).exists():
            raise serializers.ValidationError("User does not exist.")

        if score < 0:
            raise serializers.ValidationError("Score must be a non-negative integer.")

        return attrs
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.exceptions import ValidationError
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from core.models.user import User
from core.serializers.dashboard_serializer import ScoreSerializer
from core.services.leaderboard_service import LeaderBoardService

class ScoreView(APIView):

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def post(self, request):
        """
            API endpoint for submitting scores.
        """

        serializer = ScoreSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            score = serializer.validated_data['score']
            user_id = serializer.validated_data['user_id']

            # Logic to submit score to leaderboard service
            leaderboard_service = LeaderBoardService()
            leaderboard_service.submit_score(
                user_id,
                score
            )

            return Response({"result": "done"}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RankView(APIView):

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request, user_id):
        """
            API endpoint for getting rank of a user.
            /api/leaderboard/rank/<user_id>/
        """

        try:
            if not User.objects.filter(id=user_id, is_deleted=False).exists():
                return Response({"error": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)

            leaderboard_service = LeaderBoardService()
            rank = leaderboard_service.get_rank(user_id)

            if rank is None:
                return Response({"error": "Play Some Games to make mark on leaderboard"}, status=status.HTTP_404_NOT_FOUND)

            return Response({"rank": rank}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LeaderboardView(APIView):

    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        """
            API endpoint for getting leaderboard.
            /api/leaderboard/top
        """

        try:
            # Logic to get leaderboard from leaderboard service
            leaderboard_service = LeaderBoardService()
            leaderboard = leaderboard_service.get_leaderboard()

            return Response({"leaderboard": leaderboard}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

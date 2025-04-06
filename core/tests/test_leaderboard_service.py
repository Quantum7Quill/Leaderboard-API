from django.test import TestCase
from core.services.leaderboard_service import LeaderBoardService
from core.models.leaderboard import Leaderboard
from core.models.game_session import GameSession
from core.models.user import User

class LeaderBoardServiceTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create(username='testuser')

        # Create a LeaderBoardService instance
        self.service = LeaderBoardService()

    def test_submit_score_creates_game_session(self):
        # Submit a score for the user
        self.service.submit_score(self.user.id, 100)

        # Check if a game session was created
        game_sessions = GameSession.objects.filter(user_id=self.user.id)
        self.assertEqual(game_sessions.count(), 1)
        self.assertEqual(game_sessions.first().score, 100)

    def test_submit_score_updates_leaderboard(self):
        # Submit a score for the user
        self.service.submit_score(self.user.id, 100)

        # Check if the leaderboard entry was created
        leaderboard_entry = Leaderboard.objects.filter(user_id=self.user.id).first()
        self.assertIsNotNone(leaderboard_entry)
        self.assertEqual(leaderboard_entry.score, 100)

    def test_get_rank(self):
        # Submit a score for the user
        self.service.submit_score(self.user.id, 100)

        # Get the rank of the user
        rank = self.service.get_rank(self.user.id)
        self.assertEqual(rank, 1)

    def test_get_leaderboard(self):
        # Submit scores for multiple users
        user2 = User.objects.create(username='testuser2')
        self.service.submit_score(self.user.id, 100)
        self.service.submit_score(user2.id, 200)

        # Get the leaderboard
        leaderboard = self.service.get_leaderboard(limit=2)
        self.assertEqual(len(leaderboard), 2)
        self.assertEqual(leaderboard[0]['user_id'], user2.id)
        self.assertEqual(leaderboard[1]['user_id'], self.user.id)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.models.user import User
from core.models.leaderboard import Leaderboard
from core.models.game_session import GameSession

class LeaderboardViewTest(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create(username='testuser1')
        self.user2 = User.objects.create(username='testuser2')

    def test_submit_score(self):
        url = reverse('core:score')
        data = {'user_id': self.user1.id, 'score': 100}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"result": "done"})

        # Verify that the game session was created
        game_session = GameSession.objects.filter(user_id=self.user1.id).first()
        self.assertIsNotNone(game_session)
        self.assertEqual(game_session.score, 100)

    def test_get_rank(self):
        # Submit a score for the user
        Leaderboard.objects.create(user_id=self.user1.id, score=100, rank=1)

        url = reverse('core:rank', args=[self.user1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"rank": 1})

    def test_get_rank_user_not_exist(self):
        url = reverse('core:rank', args=[999])  # Non-existent user ID
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "User does not exist."})

    def test_get_leaderboard(self):
        # Submit scores for multiple users
        Leaderboard.objects.create(user_id=self.user1.id, score=100, rank=2)
        Leaderboard.objects.create(user_id=self.user2.id, score=200, rank=1)

        url = reverse('core:leaderboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['leaderboard']), 2)
        self.assertEqual(response.data['leaderboard'][0]['user_id'], self.user2.id)
        self.assertEqual(response.data['leaderboard'][1]['user_id'], self.user1.id)
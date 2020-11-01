"""Unittests for polls."""
import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from ..models import Question
from django.urls import reverse


def create_question(question_text, days):
    """
    Test that a question created properly.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=days)
    end_time = pub_time + datetime.timedelta(days=days+10)
    return Question.objects.create(question_text=question_text,
                                   pub_date=pub_time, end_date=end_time)


class AuthenticationTest(TestCase):
    """Unittest for simple user authentication"""
    def setUp(self) -> None:
        self.question = create_question(question_text="Question.", days=- 30)
        user = User.objects.create_user(username="lisbono", password="88998899")
        user.save()

    def test_vote_unauthenticated(self):
        """Unittest for voting without login"""
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_vote_authenticated(self):
        """Unittest of voting login user"""
        self.client.login(username=";lisbono", password="88998899")
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_authenticated_result(self):
        """view result page after login"""
        self.client.login(username="lisbono", password="88998899")
        url = reverse('polls:results', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

"""Unittests for polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question
from django.urls import reverse


def create_question(question_text, days, end_date):
    """
    Test that a question created properly.

    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    pub_time = timezone.now() + datetime.timedelta(days=days)
    end_time = pub_time + datetime.timedelta(days=end_date)
    return Question.objects.create(question_text=question_text,
                                   pub_date=pub_time, end_date=end_time)


class QuestionDetailViewTests(TestCase):
    """Unittests for detail page (related to Question object)."""

    def test_future_question(self):
        """Test that when asked for future question, 404 error occurred."""
        future_question = create_question(question_text='Future question.',
                                          days=5, end_date=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Test that page shown last question detail properly."""
        past_question = create_question(question_text='Past Question.',
                                        days=-5, end_date=-3)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_recent_question(self):
        """Test that page shown recent question detail properly."""
        past_question = create_question(question_text='Past Question.',
                                        days=-5, end_date=3)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
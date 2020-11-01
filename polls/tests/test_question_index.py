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


class QuestionIndexViewTests(TestCase):
    """Unittests for index page (related to Question object)."""

    def test_no_questions(self):
        """Test that there is no Question when not created any."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Test that page shown last question properly."""
        create_question(question_text="Past question.", days=-30,end_date=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Test that page doesn't show future question."""
        create_question(question_text="Future question.", days=30, end_date=35)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_'
                                                  'question_list'], [])

    def test_future_question_and_past_question(self):
        """Test that page not show future question and show last question."""
        create_question(question_text="Future question.", days=30, end_date=35)
        create_question(question_text="Past question.", days=-30, end_date=-25)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """Test that page shown multi last question properly."""
        create_question(question_text="Past question 1.", days=-30,
                        end_date=-25)
        create_question(question_text="Past question 2.", days=-5,
                        end_date=-3)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

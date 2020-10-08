"""Unittests for polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


class QuestionModelTests(TestCase):
    """Unittests for Question object."""

    def test_was_published_recently_with_future_question(self):
        """Test that future question was_publish_recently."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Test that old question was_publish_recently."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Test that recent question was_publish_recently."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59,
                                                   seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_before_publish_vote(self):
        """Test voting before publish."""
        pub = timezone.now() + datetime.timedelta(days=5)
        end = timezone.now() + datetime.timedelta(days=7)
        unpublished = Question(pub_date=pub, end_date=end)
        self.assertIs(unpublished.can_vote(), False)

    def test_after_expired_vote(self):
        """Test voting after expired."""
        pub = timezone.now() - datetime.timedelta(days=7)
        end = timezone.now() - datetime.timedelta(days=5)
        expired = Question(pub_date=pub, end_date=end)
        self.assertIs(expired.can_vote(), False)

    def test_published(self):
        """Test that the poll published."""
        pub = timezone.now() + datetime.timedelta(days=-1)
        end = timezone.now() + datetime.timedelta(days=5)
        published = Question(pub_date=pub, end_date=end)
        self.assertIs(published.is_published(), True)

    def test_unpublished(self):
        """Test that the polls not published yet."""
        pub = timezone.now() + datetime.timedelta(days=1)
        end = timezone.now() + datetime.timedelta(days=5)
        unpublished = Question(pub_date=pub, end_date=end)
        self.assertIs(unpublished.is_published(), False)


def create_question(question_text, days ,end_date):
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
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Test that page doesn't show future question."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_'
                                                  'question_list'], [])

    def test_future_question_and_past_question(self):
        """Test that page not show future question and show last question."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """Test that page shown multi last question properly."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Unittests for detail page (related to Question object)."""

    def test_future_question(self):
        """Test that when asked for future question, 404 error occurred."""
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Test that page shown last question detail properly."""
        past_question = create_question(question_text='Past Question.',
                                        days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

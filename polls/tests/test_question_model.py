"""Unittests for polls."""
import datetime
from django.test import TestCase
from django.utils import timezone
from ..models import Question


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

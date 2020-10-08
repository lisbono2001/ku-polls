"""Question and Choice object."""
import datetime
from django.db import models
from django.utils import timezone


# Create your models here.
class Question(models.Model):
    """Fields and methods for Question object."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date expired')

    def __str__(self):
        """Return question's text."""
        return self.question_text

    def was_published_recently(self):
        """Check if a specific question published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check if a specific question published."""
        return self.pub_date <= timezone.now() <= self.end_date

    def can_vote(self):
        """Check if a specific question can be voted."""
        return self.pub_date <= timezone.now() <= self.end_date

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.admin_order_field = 'end_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Fields and methods for Choice object."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice's text."""
        return self.choice_text

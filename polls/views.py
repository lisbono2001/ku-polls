"""Views for polls app' pages."""
import datetime
import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice, Vote

from django.views import generic
from django.contrib import messages

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("polls")


def get_client_ip(request):
    """ Method for getting user’s IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def check_login(request, user, **kwargs):
    """log when login success"""
    log.info("IP address: %s, %s Login at %s", get_client_ip(request), 
             user, str(datetime.now())


@receiver(user_login_failed)
def check_login_fail(request, **kwargs):
    """log when login fail"""
    log.warning("IP address: %s:  Trying to Login at %s", 
                get_client_ip(request), str(datetime.now())


@receiver(user_logged_out)
def check_logout(request, user, **kwargs):
    """log when logout success"""
    log.info("IP address: %s, %s Logout at %s", 
             get_client_ip(request), user, str(datetime.now()))


class IndexView(generic.ListView):
    """View the index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return published Question(s)."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')


class DetailView(generic.DetailView):
    """View the detail page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Return published Question(s) detail."""
        return Question.objects.filter(pub_date__lte=timezone.now())\
            .order_by('-pub_date')


class ResultsView(generic.DetailView):
    """View the result page."""

    model = Question
    template_name = 'polls/results.html'

@login_required()
def vote(request, question_id):
    """Vote mechanism for polls app."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user=request.user, question=question, defaults={'selected_choice': selected_choice})
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        date = datetime.now()
        log_vote = logging.getLogger("polls")
        log_vote.info("%s, Poll's ID: %d, at: %s.", request.user, question_id, str(date))
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


@login_required()
def polls_navigate(request, question_id):
    """Navigate to index if poll expired if not go to its detail."""
    question = Question.objects.get(pk=question_id)
    last_choice = Vote.objects.filter(question=question, user=request.user).first()
    if not question.can_vote():
        messages.warning(request, "Poll expired!, please choose another one")
        return redirect('polls:index')
    elif question.can_vote():
        return render(request, 'polls/detail.html', {'question': question,'current_choice': last_choice})

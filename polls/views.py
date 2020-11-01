"""Views for polls app' pages."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from .models import Question, Choice

from django.views import generic
from django.contrib import messages


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
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def pollsnavigate(request, question_id):
    """Navigate to index if poll expired if not go to its detail."""
    question = Question.objects.get(pk=question_id)
    if not question.can_vote():
        messages.warning(request, "Poll expired!, please choose another one")
        return redirect('polls:index')
    elif question.can_vote():
        return render(request, 'polls/detail.html', {'question': question, })

from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from polls.models import Question, Choice


#
#def index(request):
#    lates_question_list = Question.objects.all()
#    return render(request, "polls/index.html", {
#        "latest_question_list": lates_question_list
#    })


#def detail(request, question_id):
#    question = get_object_or_404(Question, pk = question_id)
#    return render(request, "polls/detail.html", {
#        "question": question
#    })

#def results(request, question_id):
#    question = get_object_or_404(Question, pk = question_id)
#    return render(request, "polls/results.html", {
#        "question": question
#    })

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        #return the last five published question
        return Question.objects.order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"



def vote(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "no elegiste una respuesta"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
        


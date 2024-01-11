from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Question


def index(req):
    question_list = Question.objects.order_by("-create_date")
    context = {"question_list": question_list}
    return render(req, "pybo/question_list.html", context)


def detail(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(req, "pybo/question_detail.html", context)


def answer_create(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(
        content=req.POST.get("content"), create_date=timezone.now()
    )
    return redirect("pybo:detail", question_id=question_id)

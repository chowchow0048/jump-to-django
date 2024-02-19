from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Answer, Question
from ..forms import AnswerForm


@login_required(login_url="common:login")
def answer_create(req, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if req.method == "POST":
        form = AnswerForm(req.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = req.user  # author 속성에 로그인 계정 저장
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            print("----question----", question.content, question.answer_set)
            print("----answer----", answer.content)
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = AnswerForm()
    context = {"question": question, "form": form}
    return render(req, "pybo/question_detail.html", context)


@login_required(login_url="common:login")
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, "수정권한이 없습니다")
        return redirect("pybo:detail", question_id=answer.question.id)
    if request.method == "POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.modify_date = timezone.now()
            answer.save()
            return redirect("pybo:detail", question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {"answer": answer, "form": form}
    return render(request, "pybo/answer_form.html", context)


@login_required(login_url="common:login")
def answer_delete(req, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if req.user != answer.author:
        messages.error(req, "삭제권한이 없습니다.")
    else:
        answer.delete()
    return redirect("pybo:detail", question_id=answer.question.id)

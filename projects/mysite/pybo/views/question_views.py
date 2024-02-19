from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..models import Question
from ..forms import QuestionForm


@login_required(login_url="common:login")
def question_create(req):
    # question_form의 submit은 action값이 없으므로, default인 현재페이지
    # 따라서 저장하기 버튼을 클릭하면, question_create 뷰 함수가 호출되고 req.method == 'POST'이다.
    if req.method == "POST":
        # print(req.POST)
        form = QuestionForm(req.POST)
        if form.is_valid():  # 폼이 유효하다면
            question = form.save(
                commit=False
            )  # 임시 저장하여 question 객체를리턴 받는다
            question.author = req.user
            question.create_date = timezone.now()  # 작성일시
            question.save()  # 데이터를 저장
            return redirect("pybo:index")  # question_list로 redirect
    else:
        form = QuestionForm()

    context = {"form": form}
    # print(req)
    return render(req, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_modify(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if req.user != question.author:
        messages.error(req, "수정권한이 없습니다.")
        return redirect("pybo:detail", question_id=question_id)

    if req.method == "POST":
        form = QuestionForm(req.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()
            question.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {"form": form}
    return render(req, "pybo/question_form.html", context)


@login_required(login_url="common:login")
def question_delete(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if req.user != question.author:
        messages.error(req, "삭제권한이 없습니다.")
        return redirect("pybo:detail", question_id=question.id)
    question.delete()
    return redirect("pybo:index")

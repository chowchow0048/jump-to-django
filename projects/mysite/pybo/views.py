from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.core.paginator import Paginator


def index(req):
    page = req.GET.get("page", "1")  # 페이지
    question_list = Question.objects.order_by("-create_date")
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    context = {"question_list": page_obj}
    # print("paginator:", paginator)
    print(paginator.num_pages)
    return render(req, "pybo/question_list.html", context)


def detail(req, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {"question": question}
    return render(req, "pybo/question_detail.html", context)


def answer_create(req, question_id):
    """
    pybo 답변 등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if req.method == "POST":
        form = AnswerForm(req.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect("pybo:detail", question_id=question.id)
    else:
        return HttpResponseNotAllowed("Only POST is possible.")
    context = {"question": question, "form": form}
    return render(req, "pybo/question_detail.html", context)

    # question = get_object_or_404(Question, pk=question_id)
    # # question.answer_set.create(
    # #     content=req.POST.get("content"), create_date=timezone.now()
    # # )
    # answer = Answer(
    #     question=question, content=req.POST.get("content"), create_date=timezone.now()
    # )
    # answer.save()

    # return redirect("pybo:detail", question_id=question_id)


def question_create(req):
    # question_form의 submit은 action값이 없으므로, default인 현재페이지
    # 따라서 저장하기 버튼을 클릭하면, question_create 뷰 함수가 호출되고 req.method == 'POST'이다.
    if req.method == "POST":
        print(req.POST)
        form = QuestionForm(req.POST)
        if form.is_valid():  # 폼이 유효하다면
            question = form.save(commit=False)  # 임시 저장하여 question 객체를리턴 받는다
            question.create_date = timezone.now()  # 작성일시
            question.save()  # 데이터를 저장
            return redirect("pybo:index")  # question_list로 redirect
    else:
        form = QuestionForm()

    context = {"form": form}
    # print(req)
    return render(req, "pybo/question_form.html", context)

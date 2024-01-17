from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question  # 사용할 모델
        fields = ["subject", "content"]  # QuestionForm에서 사용할 Question 모델의 속성
        # widgets = {  # 입력 필드에 부트스트랩 클래스 추가하기
        #     "subject": forms.TextInput(attrs={"class": "form-control"}),
        #     "content": forms.Textarea(attrs={"class": "form-control", "rows": 10}),
        # }
        labels = {
            "subject": "제목",
            "content": "내용",
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ["content"]
        labels = {"content": "답변"}

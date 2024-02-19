from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    """
    제목(subject), 내용(content), 작성일시(create_date)
    를 속성으로 갖는 모델
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

    # __str__ 메서드를 추가하면 id 값 대신 제목을 표시할 수 있다.
    def __str__(self):
        return self.subject


class Answer(models.Model):
    """
    질문에 대한 답변이므로, Qeustion 모델을 속성으로 갖는다
    Question 모델을 ForeignKey로서 연결한다.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)

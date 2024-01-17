# jump-to-django

============================
DAY1
============================
-------------------- 2장 시작 --------------------

mkdir jdj
python -m venv .venv
source .venv/bin/activate
mkdir jump-to-django

django-admin startproject config .
python manage.py runserver

비주얼 스튜디오 코드를 사용할 경우 내장 터미널이 파워셸로 실행된다. 파워셸을 사용할 경우 이 책에서 사용하는 환경 변수들이 정상적으로 설정되지 않으므로 파워셸 대신 명령창을 사용하여 이 책의 예제를 실행할 것을 당부한다.

vi .zshrc
alias jdj='cd /Users/chow/Documents/GitHub/jdj/jump-to-django/projects/mysite;source /Users/chow/Documents/GitHub/jdj/.venv/bin/activate'
source ~/.zshrc

jdj >> activate venv
django-admin startapp pybo

config/urls.py: path('pybo/', views.index)
pybo/views.py: def index(){}

"""장고 개발 흐름"""

1.  브라우저에서 로컬 서버로 http://localhost:8000/pybo 페이지를 요청
2.  urls.py 파일에서 /pybo URL 매핑을 확인하여 views.py 파일의 index함수를 호출하고
3.  호출한 결과를 브라우저에 반영한다.

python manage.py migrate: config/settings.py를 보면 django에서 기본적으로 설치한 앱들을 볼 수 있다.

SQLite는 주로 개발용이나 소규모 프로젝트에서 사용되는 가벼운 파일 기반의 데이터베이스이다. 개발시에는 SQLite를 사용하여 빠르게 개발하고 실제 운영시스템은 좀 더 규모있는 DB를 사용하는 것이 일반적인 개발 패턴이다.

ORM
전통적으로 데이터베이스를 사용하는 프로그램들은 데이터베이스의 데이터를 조회하거나 저장하기 위해 쿼리문을 사용해야 했다. 이 방식은 여전히 많이 사용되고 있는 방식이지만 몇 가지 단점이 있다. 개발자마다 다양한 쿼리문이 만들어지고, 또 잘못 작성된 쿼리는 시스템의 성능을 저하 시킬수 있기 때문이다. 그리고 데이터베이스를 MySQL에서 오라클로 변경하면 프로그램에서 사용한 쿼리문을 모두 해당 데이터베이스의 규칙에 맞게 수정해야 하는 어려움도 생긴다.
ORM(Object Relational Mapping)을 사용하면 데이터베이스의 테이블을 모델화하여 사용하기 때문에 위에서 열거한 SQL방식의 단점이 모두 없어진다. ORM을 사용하면 개발자별로 독특한 쿼리문이 만들어질 수가 없고 또 쿼리를 잘못 작성할 가능성도 낮아진다. 그리고 데이터베이스 종류가 변경되더라도 쿼리문이 아닌 모델을 사용하기 때문에 프로그램을 수정할 필요가 없다.

django ORM field types
https://docs.djangoproject.com/en/4.0/ref/models/fields/#field-types

pybo/models.py: class Question(models.Model), class Answer(models.Model)
만들고 python3 manage.py makemigrations >> pybo/migrations 폴더 생성!
""모델을 생성하거나 모델에 변화가 있을 경우 makemigrations 해줘야함""

sqlmigrate
python3 manage.py sqlmigrate pybo 0001: 실행되는 쿼리들을 조회한다. 실제로 쿼리가 수행되는것은 아님

============================
DAY2
============================
python3 manage.py sqlmigrate
python3 manage.py migrate
python3 manage.py shell

<Question 생성 조회 수정 삭제>
from pybo.models import Question, Answer
from django.utils import timezone

<생성>
q = Question(question='ASFASDF?', content='asdfjaksnrgljasrg', create_date=timezone.now())
q.save()
q.id

<조회>
Question.objects.all()
Question.objects.filter(id=1?)
Question.objects.get(id=1?)
Quesiion.objects.filter(subject\_\_contains='찾고싶은 단어나 문장 글자도되고')

<수정>
q = Question.objects.get(id=2)
q.subject = '바꾸고싶은 제목'
q.save() >> save해야 적용된데

<삭제>
q.delete()
Question.objects.all() >> 조회하면 삭제되어있음

<장고 관리자>
python3 manage.py createsuperuser >> admin 계정을 만들수있음

pybo/admin.py 에서
from .models import Question

admin.site.register(Question)
하면 localhost:8000/admin 가서 직접 테이블을 CRUD할 수 이씀

<조회와 템플릿>
mysite/templates, mysite/templates/pybo 만듬
template은 html인데 {{}} 를 써서 객체를 출력하거나 {% %}를 써서 반복문이나 조건문을 적용할 수 있다

urls.py에서 새로운 path를 뚫고
views.py에서 path에 매핑할 함수를 만들고
함수에서 render할 템플릿을 만든다

from django.shortcuts import get_object_or_404
get_object_or_404(Question, pk=question_id)
: localhost:8000/pybo/141424 같이 없는 데이터를 요청할 경우 에러코드 500이 아닌 404를 보내는 방법

<URL별칭>
url의 리펙토링이 빈번히 일어나면 템플릿에 href로 박혀있는 url들을 일일히 바꿔줘야하는 불상사가 발생할수있다 >> URL별칭 사용

path('', views.index, name='index'),
path('<int:question_id>/', views.detail, name='detail')
name='어쩌구' 를 통해 URL별칭을 부여할수있다, 이렇게하면
템플릿에서 별칭을 사용해 하드코딩된 url을 변경할수있다
<a href='{% url 'detail' quesiont.id %}'> (뭔가 와닿지않는다)

<URL namespace>
프로젝트가 커져서 URL별칭도 중복이 될수있음. 그래서 하나 더 큰 이름을 붙여서 분류해줘야함 그게 네임스페이스임

pybo/urls.py 에서 app_name = 'pybo' 해주고
템플릿가서 '{% url 'pybo:detail' question.id %}' 이렇게 바꿔주면 됨

URL 별칭이랑 네임스페이스는 redirect할 때도 쓰임

============================
DAY3
============================
<데이터 저장>
방법 2개있음.

1. Question이 Answer랑 ForeingKey로 연결되어있기 때문에
   question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())

2. Answer 모델을 사용
   answer = Answer(question=question, content=request.POST.get('content'), create_date=timezone.now())
   answer.save()

<스태틱>
화면에 디자인 적용하기 > css 사용

1. config/settings.py에서 스태틱 파일에 대한 BASEDIR 지정
   (config/settings.py)
   STATIC_URL = "static/"
   STATICFILE_DIRS = [
   BASE_DIR / "static",
   ]

2. static 폴더 생성 (mysite 하위)

3. style.css 생성 (mysite/static/style.css)

4. style.css 적용할 템플릿에서 스타일 적용
(question_detail.html)
{% load static %}
<link rel='stylesheet' type="text/css" href="{% static 'style.css' %}">

<BootStrap>
1. Bootstrap 다운로드
2. static/ 에 bootstrap.min.css 복붙
3. 템플릿들에 <link> 태그로 적용
4. 디자인적용

<Base html>
1. 템플릿의 기초가 될 html을 만들자 (template/base.html, template/pybo/가 아님)
2. base.html은 내가 잘 아는 html 기본형식(doctype html - head - body)인데, 맨 위에 {% load static %}, body부분에 {% block content %} - {% endblock %} 형식으로 컨텐츠들을 디스플레이함
3. block content에 들어갈 템플릿들은 html의 시작에 {% extends 'base.html'%} {% block content %} 를 쓰고, 마지막 라인에 {% endblock %} 을 써준다

============================
DAY4
============================

<Form>
Form: 페이지 요청 시, 전달되는 파라미터들을 쉽게 관리하기 위해 사용하는 Class
1. form이 보일 화면으로 가는 버튼 만들기
<a href="{% url 'pybo:question_create' %}">질문 등록</a>

2. url 매핑
   path('question/create/', views.question_create, name='question_create'),

3. forms.py 만들기 (mysite/pybo/forms.py)

4. 패키지 import
   from django import forms
   from pybo.models import Question

5. forms.ModelForm vs forms.Form
   ModelForm은 model과 연결된 폼으로 폼을 저장하면 연결된 모델의 데이터를 저장할 수 있다, 모델 폼은 inner class인 Meta class가 반드시 필요하다. Meta class에는 사용할 모델과 속성을 적어야한다.

   class QuestionForm(forms.ModelForm):
   class Meta:
   model = Question # 사용할 모델
   fields = ['subject', 'content'] # QuestionForm에서 사용할 Question 모델의 속성

6. 뷰 함수 만들기
   from .forms import QuestionForm

   def question_create(req):
   form = QuestionForm

   return render(req, "pybo/question_form.html", {'form': form})

req: 함수의 첫번째 매개변수, 클라이언트로부터의 정보를 담고있다. question_list에 있는 pybo/question/create/ 로 이동하는 a태그를 클릭하면, <WSGIRequest: GET '/pybo/question/create/'> 라는 정보를 담게 된다.

render(): 매개변수를 토대로 화면을 렌더링하는 django 내장 함수. render함수는 req, 렌더링할 경로, 템플릿에 전달할 데이터가 필요하다. 템플릿에 전달할 데이터는 주로 딕셔너리 형태로 이루어져있는데, 이는 모델 인스턴스, 쿼리셋, 폼 인스턴스, 기타 컨텍스트 데이터 등이 될 수있다. 뷰 함수에서 템플릿으로 이러한 데이터들을 전달해야 템플릿에서 완성된 화면을 사용자에게 전달할 수 있다.

7. 뷰 함수 완성
   def question_create(req):

   # question_form의 submit은 action값이 없으므로, default인 현재페이지

   # 따라서 저장하기 버튼을 클릭하면, question_create 뷰 함수가 호출되고 req.method == 'POST'이다.

   if req.method == 'POST':
   form = QuestionForm(req.POST)

   if form.is_valid(): # 폼이 유효하다면
   question = form.save(commit=False) # 모델 임시 저장
   question.create_date = timezone.now()
   question.save() # 데이터 저장
   return redirect('pybo:index')

   else:
   question = QuestionForm() # request 메서드가 GET일 때

   context = {'form': form}

   return render(req, 'pybo/question/create', context)

============================
DAY5 2장 끝
============================

<Form 2>

form widget: form에 스타일 적용하는 방법, {{ form.as_p }}를 써서 자동으로 폼을
만들때 사용하기 좋다.
[projects/mysite/pybo/forms.py]
class QuestionForm(forms.ModelForm):
class Meta:
model = Question
fields = ['subject', 'content']
widgets = {
'subject': forms.TextInput(attrs={'class': 'form-control'}),
'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10})
}

하지만 {{ form.as_p }}를 통해 만든 자동 폼은 디자인 수정이 귀찮고 제한적이다.
따라서 수동으로 폼을 만드는 방법을 알아야한다

1. 템플릿 만들기(question_form.html을 수정할거임)
   a. 에러 체크
   {% if form.errors %}
   <div class='alert alert-danger' role='alert'> 
        {% form field in form %}
        {% if field.errors %}
        <div>
            <strong>{{ field.label }}</strong>
            {{ field.errors }}
        </div>
        {% endif %}
        {% endfor %}
   </div>
   {% endif %}

   b. form 만들기
   <div class='mb-3'>
        <label for='subject' class='form-label'>제목</label>
        <input type='text' class='form-control' name='subject' id='subject' value='{{ form.subject.value|default_if_none:''}}'> 
   </div>
   <div>
        <label for='content' class='form-label'>내용</label>
        <textarea class='form-control' name='content id='content'  rows='10'>{{form.content.value|default_if_none:''}}</textarea>
   </div>

   총 두단계,에러체킹과 실제 폼 제작
   에러체킹은 만들고자 하는 폼의 개수에 따라 각 폼이 비었는지 확인하는 작업이다. 뭔가 조건을 더 걸어서 할 수도 있을거같은 느낌이드는데..
   form 만드는건 (라벨 + 인풋) 인데, 인풋 부분에서 ~.value|default_if_none:'' 이 부분이 특수하다. 해석하자면 ~의 value가 none 일 때의 기본값은:'' 이라는 뜻, 즉 빈값이면 None 대신 공백으로 표시하라는 의미의 <템플릿 필터> 이다

-------------------- 2장 종료 --------------------
-------------------- 3장 시작 --------------------

<내비게이션 바>

부트스트랩의 내비게이션 바 사용, 음...부트스트랩 클래스들을 마구때려박아서 navbar를 만들었음. 잘라놨다가 복붙해서 쓰는게 좋아보임

<!-- <include>

django에는 템플릿의 특정 위치에 다른 템플릿을 삽입할 수 있는 include 태그가 있다.
템플릿에서 특정 구간이 반복적으로 사용될 때 중복을 없애기 위해 사용. -->

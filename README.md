# jump-to-django

practice
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

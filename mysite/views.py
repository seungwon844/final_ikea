from django.views.generic.base import TemplateView

# 아래 3줄 11장 추가
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse_lazy

# TemplateView 제네릭 뷰를 상속받아서 HomeView 클래스 작성
class HomeView(TemplateView):
	# TemplateView를 상속받을 때 template_name 클래스 변수 오버라이딩은 필수
	# 템플릿 파일의 이름을 지정하는데, 파일의 위치는 settings.TEMPLATES.DIRS 항목에서 정의함
	template_name = 'home.html'

# 11장 추가
class UserCreateView(CreateView):
	template_name = 'registration/register.html'
	form_class = UserCreationForm
	success_url = reverse_lazy('register_done')
class UserCreateDoneTV(TemplateView):
	template_name = 'registration/register_done.html'

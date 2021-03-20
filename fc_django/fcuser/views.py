from django.shortcuts import render ,redirect
from django.views.generic.edit import FormView
from .forms import RegisterForm, LoginForm
from django.contrib.auth.hashers import make_password
from .models import Fcuser

# Create your views here.

def index(request):
    return render(request,'index.html',{'email' : request.session.get('user')})


class RegisterView(FormView):
    template_name =  'register.html'
    form_class = RegisterForm
    #url을 이동시킬 수 있음
    success_url = '/'

    #유효하다면 form_valid 함수를 사용해 db에 저장
    def form_valid(self, form):
        fcuser = Fcuser(
            email = form.data.get('email'),
            password = make_password(form.data.get('password')),
            level = 'user'
        )

        return super().form_valid(form)

class LoginView(FormView):
    template_name =  'login.html'
    form_class = LoginForm
    #url을 이동시킬 수 있음
    success_url = '/'

    #form_valid라는 함수로 session에 저장
    def form_valid(self, form):
        self.request.session['user']=form.data.get('email')
        

        return super().form_valid(form)
    
def logout(request):
    if 'user' in request.session :
        del(request.session['user'])

    return redirect('/')
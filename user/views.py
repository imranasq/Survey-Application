from django.http import HttpResponse
from .forms import UserLoginForm, SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView
from django.views import generic

from rest_framework import viewsets
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
class SignUpView(generic.CreateView):
    template_name = 'user/register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"


class LoginView(View):
    model = User
    template_name = "user/login.html"

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_admin:
                login(request, user)
                return HttpResponseRedirect('/admin-panel')
            elif user.user_type=="Customer":
                login(request, user)
                return redirect('/customer-panel')
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect('/login')

    def get(self, request):
        next = request.GET.get('next')
        form = UserLoginForm(request.POST or None)
        context = {
            'login_form': form,
           }
        return render(request, "user/login.html", context)

class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer
    queryset = User.objects.all()

@login_required(login_url='login')
def hello(request):
    return HttpResponse('Hello World')


class AdminPanelView(TemplateView):
    model = User
    template_name = "user/admin-panel.html"

    def get_context_data(self, **kwargs):
        filtered_user = User.objects.filter(email=self.request.user.email)
        if filtered_user.exists():
            users = filtered_user
        context = {
            'users': users
        }
        return context

class CustomerPanelView(TemplateView):
    model = User
    template_name = "user/customer-panel.html"

    def get_context_data(self, **kwargs):
        filtered_user = User.objects.filter(email=self.request.user.email)
        if filtered_user.exists():
            users = filtered_user
        context = {
            'users': users
        }
        return context

def logout_view(request):
    logout(request)
    return redirect('/')
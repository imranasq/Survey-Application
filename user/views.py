from django.http import HttpResponse
from .forms import UserLoginForm, SignUpForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.messages.views import SuccessMessageMixin
from .models import User
from django.urls import reverse_lazy
from django.views.generic import View
from django.views import generic

from rest_framework import viewsets
from .serializers import LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
class SignUpView(generic.CreateView):
    template_name = 'register.html'
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    success_message = "Your profile was created successfully"


class LoginView(View):
    model = User
    template_name = "login.html"

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
        return render(request, "login.html", context)

class UserView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = LoginSerializer
    queryset = User.objects.all()

@login_required(login_url='login')
def hello(request):
    return HttpResponse('Hello World')

@login_required(login_url='login')
def AdminHomeView(request):
    context = {}
    admin_obj = User.objects.filter(email = request.user.email)
    context = {
        'users' : admin_obj,
    }
    return render(request, "admin-panel.html", context)

@login_required(login_url='login')
def CustomerHomeView(request):
    context = {}
    customer_obj = User.objects.filter(email = request.user.email)
    context = {
        'users' : customer_obj,
    }
    return render(request, "customer-panel.html", context)
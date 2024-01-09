from django.views.generic import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

from task.forms import TaskForm, RegisterForm
from task.models import Task

def logOut(request):
    logout(request)
    return redirect('home')

class HomeView(TemplateView):
    template_name = "home.html"
    form_class = TaskForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            n = form.cleaned_data['name']
            des = form.cleaned_data['description']
            d = form.cleaned_data['date']

            t = Task.objects.create(
                user=request.user,
                name=n,
                description=des,
                date=d,
            )

            return redirect('home')

class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        u = authenticate(request, username=username, password=password)
        if u is not None: 
            login(request, u)
            return redirect('home')
        print(str(username) + ' ' + str(password))
        print("user " + str(u))
        return redirect('login')

class RegisterView(TemplateView):
    template_name = "register.html"
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            u = User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            u.set_password(form.cleaned_data['password'])
            u.save()

            login(request, u)
            return redirect('home')

        return redirect('register')
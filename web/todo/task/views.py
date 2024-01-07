from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse

from task.forms import TaskForm
from task.models import Task

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

            return render(request, self.template_name, {'form':TaskForm()})
from django.urls import path

from .views import *

urlpatterns = [
    path('get-tasks/', getTasks),
    path('task-btn/', taskBtn),
]

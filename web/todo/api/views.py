from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from task.models import Task
from .serializers import TaskSerializer

from datetime import datetime

@api_view(['GET'])
def getTasks(request):
    # TODO Authentication

    date = request.GET.get('date')
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    serializer = TaskSerializer(Task.objects.filter(date=date.date()), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def taskBtn(request):
    # TODO Authentication
    t = request.GET.get('type')
    id = request.GET.get('id')

    try:    
        task = Task.objects.get(id=id)
        if t == "don":
            task.done = True
            task.save()
        elif t == "del": 
            task.delete()
    except Exception as e: print(e)

    return Response(status=status.HTTP_200_OK)
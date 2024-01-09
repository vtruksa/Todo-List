from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from task.models import Task
from .serializers import TaskSerializer

from datetime import datetime

@api_view(['GET'])
def getTasks(request):
    date = request.GET["date"]
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

    serializer = TaskSerializer(Task.objects.filter(date=date.date()), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
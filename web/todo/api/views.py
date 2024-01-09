from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from task.models import Task
from .serializers import TaskSerializer

@api_view(['GET'])
def getTasks(request):
    print("API called")
    serializer = TaskSerializer(Task.objects.all(), many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
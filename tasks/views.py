from rest_framework import generics

from .models import Task
from .permissions import IsAuthorOrReadOnly 
from .serializers import TaskSerializer
from rest_framework.response import Response
from .task1 import send_email_task
from rest_framework import status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication


class TaskList(generics.ListCreateAPIView):
    permission_classes = (IsAuthorOrReadOnly, BasicAuthentication, SessionAuthentication) 
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user or self.request.user.is_superuser)

    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = TaskSerializer(queryset, many=True, fields=('id', 'title', 'deadline'))
        return Response(serializer.data)
        

class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrReadOnly,)  
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def get_queryset(self):
        return super().get_queryset().filter(author=self.request.user or self.request.user.is_superuser)
    
    def post(self, request, pk):
        task = Task.objects.get(id=pk)
        task.completed = not task.completed
        task.save()

        subject = "Task status update"
        message = "Task has been marked as completed" if task.completed else "Task has been un-marked as completed"
        from_email = "noreply@example.com"
        recipient_list = [task.author.email]

        send_email_task.delay(subject, message, from_email, recipient_list)
        return Response({"status": "success"})

    def put(self, request, pk):
        task = Task.objects.get(id=pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


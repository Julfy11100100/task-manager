from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import TasksSerializer
from rest_framework import permissions
from .models import Task
from .permissions import IsUser


class TasksList(ListCreateAPIView):

    serializer_class = TasksSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TasksDetailList(RetrieveUpdateDestroyAPIView):
    serializer_class = TasksSerializer
    queryset = Task.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsUser, )
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
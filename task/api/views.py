from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import ReadOnlyTasksSerializer, WriteOnlyTasksSerializer
from .models import Task


class GetAllTasksView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ReadOnlyTasksSerializer
    queryset = Task.objects.all()

    def get(self, request):
        email = request.user
        tasks = self.get_queryset().filter(user__email=email)
        serializer = self.serializer_class(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateTaskView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = WriteOnlyTasksSerializer
    queryset = Task.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetTaskByIdView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ReadOnlyTasksSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        try:
            email = request.user
            task = self.get_queryset().get(user__email=email, id=pk)
            serializer = self.serializer_class(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"Id does not exists"}, status=status.HTTP_404_NOT_FOUND)


class SetTaskAsCompleteView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = ReadOnlyTasksSerializer
    queryset = Task.objects.all()

    def get(self, request, pk):
        try:
            email = request.user
            task = self.get_queryset().get(user__email=email, id=pk)
            task.is_complete = True
            task.save()
            serializer = self.serializer_class(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"Id does not exists"}, status=status.HTTP_404_NOT_FOUND)


class DeleteTaskView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = WriteOnlyTasksSerializer
    queryset = Task.objects.all()

    def delete(self, request, pk):
        try:
            email = request.user
            task = self.get_queryset().get(user__email=email, id=pk)
            task.delete()
            return Response({"Task was successfully deleted"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"Id does not exists"}, status=status.HTTP_404_NOT_FOUND)
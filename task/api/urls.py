from django.urls import path
from . import views

urlpatterns = [
    path('', views.TasksList.as_view(), name='tasks'),
    path('<int:id>', views.TasksDetailList.as_view(), name='task'),
]
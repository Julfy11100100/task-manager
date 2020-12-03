from django.urls import path
from . import views

urlpatterns = [
    path('tasks/', views.GetAllTasksView.as_view(), name='tasks'),
    path('create_task/', views.CreateTaskView.as_view(), name='create_task'),
    path('task_by_id/<int:pk>', views.GetTaskByIdView.as_view(), name='task_by_id'),
    path('set_as_complete/<int:pk>', views.SetTaskAsCompleteView.as_view(), name='set_as_complete'),
    path('delete_task/<int:pk>', views.DeleteTaskView.as_view(), name='delete_task'),
]
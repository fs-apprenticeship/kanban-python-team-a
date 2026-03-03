from django.urls import path
from . import views

urlpatterns = [
    path('<int:task_id>/delete/', views.task_delete, name='task-delete'),
]

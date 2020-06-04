from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>/', views.board, name='board'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update-task/', views.update_task_state),
    path('create-task/', login_required(views.CreateTask.as_view())),
    path('create-board/', login_required(views.CreateBoard.as_view()))
]

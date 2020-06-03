from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('board/<int:board_id>/', views.board, name='board'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('update-task/', views.update_task_state),
    path('create-task/', views.create_task)
]

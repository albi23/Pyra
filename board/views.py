from typing import List

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
# Create your views here.
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from board.forms import SignUpForm
from .models import Board
from .models import Task


@login_required
def index(request):
    _all_boards = Board.objects.filter(members=request.user)
    board_col1: List[Board] = [_all_boards[i] for i in range(0, len(_all_boards), 3)]
    board_col2: List[Board] = [_all_boards[i] for i in range(1, len(_all_boards), 3)]
    board_col3: List[Board] = [_all_boards[i] for i in range(2, len(_all_boards), 3)]

    context = {
        'board_col1': board_col1,
        'board_col2': board_col2,
        'board_col3': board_col3,
    }
    return render(request, 'index.html', context)


@login_required
def board(request, board_id):
    _board = Board.objects.get(id=board_id)
    todo_tasks = Task.objects.filter(board=_board, status='TODO')
    doing_tasks = Task.objects.filter(board=_board, status='DOING')
    done_tasks = Task.objects.filter(board=_board, status='DONE')

    context = {
        'board': _board,
        'todo_tasks': todo_tasks,
        'doing_tasks': doing_tasks,
        'done_tasks': done_tasks
    }

    return render(request, 'board.html', context)


@login_required
@csrf_exempt
def update_task_state(request):
    if request.method == "POST":
        task_id = request.POST['id']
        new_state = request.POST['state']
        this_task = Task.objects.get(id=task_id)
        this_task.status = new_state
        this_task.save()

        return JsonResponse({"success": "true"})


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

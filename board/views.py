from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from board.forms import SignUpForm
from .models import Board
from .models import Task
from .const import BOARD_VIEW_COLUMN_COUNT


@login_required
def index(request):
    board_col, row_count = Board.objects.get_user_split_boards(request.user, BOARD_VIEW_COLUMN_COUNT)

    context = {
        'board_col': board_col,
        'row_count': row_count
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
        task_id = request.POST['task_id']
        new_state = request.POST['new_state']
        this_task = Task.objects.get(id=task_id)
        this_task.status = new_state
        this_task.save(force_update=True)

    return JsonResponse({"success": "true"})


@login_required
@csrf_exempt
def create_task(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        state = request.POST['state']
        priority = request.POST['priority']

        print(title)
    return JsonResponse({"success": "true"})


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class CreateBoard(generic.CreateView):
    pass


class CreateTask(generic.CreateView):
    pass

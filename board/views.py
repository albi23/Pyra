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
    context = {
        'boards': Board.objects.all()
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

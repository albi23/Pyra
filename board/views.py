from typing import List

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic, View

from board.forms import SignUpForm
from .const import BOARD_VIEW_COLUMN_COUNT
from .models import Board, Priority, Membership, Contribution
from .models import Task


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
    todo_tasks: List[Task] = Task.objects.filter(board=_board, status='TODO')
    doing_tasks = Task.objects.filter(board=_board, status='DOING')
    done_tasks = Task.objects.filter(board=_board, status='DONE')

    context = {
        'board': _board,
        'todo_tasks': todo_tasks,
        'doing_tasks': doing_tasks,
        'done_tasks': done_tasks,
        'user': request.user,
    }

    return render(request, 'board.html', context)


@login_required
def update_task_state(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        new_state = request.POST['new_state']
        this_task = Task.objects.get(id=task_id)
        this_task.status = new_state
        this_task.save()

    return JsonResponse({"success": True})


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class CreateBoard(View):

    def post(self, request):
        name = request.POST['name']
        description = request.POST['description']

        if name:
            new_board = Board.objects.create(
                name=name,
                description=description,
            )
            Membership.objects.create(
                board=new_board,
                user=request.user,
                role=Membership.Role.SUPER_USER
            )

            return JsonResponse({"success": True})

        return JsonResponse({"success": False})


class CreateTask(View):

    def post(self, request):
        title = request.POST['title']
        description = request.POST['description']
        status = request.POST['status']
        priority = int(request.POST['priority'])
        board_id = int(request.POST['board_id'])

        if title and request.user in Board.objects.get(id=board_id).members.all():
            Task.objects.create(
                title=title,
                description=description,
                status=status,
                priority=Priority.choices[-int(priority) - 1][0],
                created_by=request.user,
                board_id=board_id
            )

            return JsonResponse({"success": True})

        return JsonResponse({"success": False})


class CreateBoardMembership(View):

    def post(self, request):
        username = request.POST['username']
        board_id = int(request.POST['board_id'])

        if username and board_id:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse(
                    status=404,
                    data={'message': 'User doesn\'t exist'}
                )

            try:
                membership = Membership.objects.get(board=board_id, user=user.id)
            except Membership.DoesNotExist:
                membership = None

            if membership is not None:
                return JsonResponse(
                    status=400,
                    data={'message': 'user already added'}
                )

            Membership.objects.create(
                user=user,
                board_id=board_id
            )
            return JsonResponse({'message': 'success'})

        return JsonResponse(
            status=400,
            data={'message': 'username or board_id can\'t be empty'}
        )


def parse_priority(value: str):
    choices = Priority.choices
    for i in range(0, len(choices)):
        if value == choices[i][1].lower():
            return choices[i][0]


@login_required
def update_task(request):
    this_task = Task.objects.get(id=request.POST['id'])
    this_task.title = request.POST['title']
    this_task.description = request.POST['description']
    this_task.status = request.POST['status']
    this_task.priority = parse_priority(request.POST['priority'].lower())
    this_task.save()

    assigned_user_id = request.POST['user']
    if assigned_user_id:
        Contribution.objects.create(
            task=this_task,
            user_id=assigned_user_id,
        )

    return JsonResponse({"success": True})


@login_required
def get_available_users(request):
    users = User.objects.filter(
        membership__board_id=request.GET['board']
    ).exclude(
        contribution__task_id=request.GET['task']
    )
    response_users = list(map(
        lambda user: {
            'id': user.id,
            'username': user.username
        },
        users
    ))

    return JsonResponse({'users': response_users})


@login_required
def delete_task(request):
    if request.method.POST['task']:
        task = Task.objects.get(id=request.method.GET['task'])
        if request.user in task.board.members.all():
            task.delete()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False})

from typing import List

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic, View

from board.forms import SignUpForm
from .const import BOARD_VIEW_COLUMN_COUNT
from .models import Board, Priority, Membership
from .models import Task


@login_required
def index(request):
    board_col, row_count = Board.objects.get_user_split_boards(request.user, BOARD_VIEW_COLUMN_COUNT)

    context = {
        'board_col': board_col,
        'row_count': row_count
    }
    return render(request, 'index.html', context)


# extension method to User class
def get_initials(self) -> str:
    name: str = self.first_name
    last_name: str = self.last_name

    if name is None or len(name) < 1 \
            or last_name is None or len(last_name) < 1:
        user = self.username.upper()
        return user if len(user) <= 2 else user[:2]

    return (name[:1] + last_name[:1]).upper()


auth.models.User.add_to_class('get_initials', get_initials)


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
        'done_tasks': done_tasks
    }

    return render(request, 'board.html', context)


@login_required
def update_task_state(request):
    if request.method == "POST":
        task_id = request.POST['task_id']
        new_state = request.POST['new_state']
        this_task = Task.objects.get(id=task_id)
        this_task.status = new_state
        this_task.save(force_update=True)

    return JsonResponse({"success": "true"})


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
            new_board.save()

            creator_membership = Membership.objects.create(
                board=new_board,
                user=request.user,
                role=Membership.Role.SUPER_USER
            )
            creator_membership.save()

            return JsonResponse({"success": "true"})

        return JsonResponse({"success": "false"})


class CreateTask(View):

    def post(self, request):
        title = request.POST['title']
        description = request.POST['description']
        status = request.POST['status']
        priority = int(request.POST['priority'])
        board_id = int(request.POST['board_id'])

        if title and request.user in Board.objects.get(id=board_id).members.all():
            new_task = Task.objects.create(
                title=title,
                description=description,
                status=status,
                priority=Priority.choices[-int(priority) - 1][0],
                created_by=request.user,
                board_id=board_id
            )

            new_task.save()

            return JsonResponse({"success": "true"})

        return JsonResponse({"success": "false"})


class CreateBoardMembership(View):

    def post(self, request):
        username = request.POST['username']
        board_id = int(request.POST['board_id'])

        if username and board_id:
            user = User.objects.get(username=username)
            membership = Membership.objects.create(
                user=user,
                board_id=board_id
            )
            membership.save()
            return JsonResponse({"success": "true"})

        return JsonResponse({"success": "false"})


def parse_priority(value: str):
    choices = Priority.choices
    for i in range(0, len(choices)):
        if value == choices[i][1].lower():
            return choices[i][0]


@login_required
def update_task(request):
    print(request.POST['id'])
    this_task = Task.objects.get(id=request.POST['id'])
    this_task.title = request.POST['title']
    this_task.description = request.POST['description']
    this_task.status = request.POST['status']
    this_task.priority = parse_priority(request.POST['priority'].lower())
    this_task.save(force_update=True)

    return redirect('board', board_id=this_task.board_id)


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

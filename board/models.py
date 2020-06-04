import math
from typing import List

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy


def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))


class BoardManager(models.Manager):
    def get_user_split_boards(self, user, column_count):
        all_boards = self.filter(members=user)
        row_count = math.ceil(len(all_boards) / column_count)
        board_col: List[Board] = list(split(all_boards, row_count)) if row_count > 0 else []
        return board_col, row_count


class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User, through='Membership')
    objects = BoardManager()

    def __str__(self):
        return self.name


class Membership(models.Model):
    class Role(models.TextChoices):
        SUPER_USER = 'SU', gettext_lazy('Superuser')
        NORMAL = 'NO', gettext_lazy('Normal')

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.NORMAL)


class Priority(models.TextChoices):
    VERY_HIGH = 'VH', gettext_lazy('Very high')
    HIGH = 'HIGH', gettext_lazy('High')
    NORMAL = 'NORMAL', gettext_lazy('Normal')
    LOW = 'LOW', gettext_lazy('Low')
    VERY_LOW = 'VL', gettext_lazy('Very low')


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        TODO = 'TODO', gettext_lazy('To Do')
        DOING = 'DOING', gettext_lazy('Doing')
        DONE = 'DONE', gettext_lazy('Done')

    title = models.CharField(max_length=30)
    description = models.TextField(max_length=200)
    status = models.CharField(max_length=5, choices=TaskStatus.choices, default=TaskStatus.TODO)
    priority = models.CharField(max_length=6, choices=Priority.choices, default=Priority.NORMAL)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    contributors = models.ManyToManyField(User, through='Contribution', related_name='contributor')

    def __str__(self):
        res: str = "title: [" + self.title + "]" + \
                   "description:[" + self.description + "]" + \
                   "status:[" + self.status + "]" + \
                   "priority:[" + self.priority + "]" + \
                   "contributors:[" + self.contributors.__str__() + "]\n"
        return res


class Contribution(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)

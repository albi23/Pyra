import math
from typing import List

from django.contrib.auth.models import User
from django.db import models


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
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    join_date = models.DateTimeField(auto_now_add=True)


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=5)  # TODO DOING DONE
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

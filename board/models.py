from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    members = models.ManyToManyField(User, through='Membership')

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

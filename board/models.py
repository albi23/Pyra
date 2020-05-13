from django.db import models


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=5)  # TODO DOING DONE
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

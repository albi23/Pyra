from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views import generic

from board.forms import SignUpForm
from .models import Board


@login_required
def index(request):
    context = {
        'boards': Board.objects.all()
    }
    return render(request, 'index.html', context)


def board(request, board_id):
    context = {
        'board': Board.objects.get(id=board_id)
    }
    return render(request, 'board.html', context)


class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

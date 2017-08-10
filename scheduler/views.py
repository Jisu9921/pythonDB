from django.shortcuts import render
from .spreadsheets import *
# Create your views here.


def scheduler_index(request):
    return render(request, 'view/index.html')

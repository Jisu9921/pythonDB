from django.shortcuts import render
from .spreadsheets import *
# Create your views here.


def scheduler_index(request):
    print(get_sheet_name("1qEtfTDg0jn72MLDhmrUxFpJD7tzFyq-5qTySGvghKqg"))
    return render(request, 'view/index.html')

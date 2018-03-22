from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .utils import *

def homepage(request):
    pages = Page.objects.filter(menu=True)
    return render(request, 'rauwkost/homepage.html', {
        'pages': pages,
    })

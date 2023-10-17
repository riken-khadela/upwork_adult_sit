from django.shortcuts import render
from django.shortcuts import render, redirect

# Create your views here.

def data_flair(request):
    return redirect('admin/')
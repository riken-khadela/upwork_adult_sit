from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.core.management import call_command

# Create your views here.

def data_flair(request):
    return redirect('admin/')



class RunScript(View):
    def get(self, request, *args, **kwargs):
        call_command('update_conf')
        data = {
            'message': 'Call Api to dowloads the videos!',
            'status': 'success'
        }
        return JsonResponse(data)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import to_do_list_app
from to_do_list_app import models

@login_required(login_url='login')
def home(request):
    to_dos = to_do_list_app.models.Jobs.objects.filter(completed=False).order_by('item')
    context = {'to_dos' : to_dos}
    return render(request, 'home.html', context)


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html', {})
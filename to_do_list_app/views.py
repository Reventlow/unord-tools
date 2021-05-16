from django.shortcuts import render, redirect
from .models import Jobs
from .forms import ListForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='login')
def todo(request):
    if request.method == 'POST':
        form = ListForm(request.POST or None)
        if form.is_valid() and request.POST['item'] != '':
            form.save()
            all_items = Jobs.objects.all
            messages.success(request, request.POST['item']+ ' er blevet tilføjet til din opgave list')
            context = {'all_items': all_items}
            return render(request, 'todo.html', context)
    else:
        all_items =Jobs.objects.all
        context = {'all_items': all_items}
        return render(request, 'todo.html', context)

@login_required(login_url='login')
def delete(request, job_id):
    item = Jobs.objects.get(pk=job_id)
    item.delete()
    messages.success(request, 'Opgaven er blevet slettet fra din opgave list')
    return redirect('todo')

@login_required(login_url='login')
def cross_off(request, job_id):
    item = Jobs.objects.get(pk=job_id)
    item.completed = True
    messages.success(request, 'Opgaven er løst, hvor er du bare mega sej')
    item.save()
    return redirect('todo')

@login_required(login_url='login')
def uncross(request, job_id):
    item = Jobs.objects.get(pk=job_id)
    item.completed = False
    messages.success(request, 'Opgaven var ikke helt løst, no worries det handler bare om at give den en skalle ;-)')
    item.save()
    return redirect('todo')

@login_required(login_url='login')
def edit(request, job_id):
    if request.method ==  'POST':
        item = Jobs.objects.get(pk=job_id)
        form = ListForm(request.POST or None, instance=item)
        if form.is_valid() and request.POST['item'] != '':
            form.save()
            all_items = Jobs.objects.all
            messages.success(request, request.POST['item']+ ' er blevet redigeret i din opgave list')
            return redirect('todo')
    else:
        item =Jobs.objects.get(pk=job_id)
        context = {'item': item}
        return render(request, 'edit.html', context)







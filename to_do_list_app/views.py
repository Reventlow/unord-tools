from django.shortcuts import render, redirect
from .models import Jobs
from .forms import JobsForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from . import models
from . import forms




# Create your views here.

@login_required(login_url='login')
def todo(request):
    if request.method == 'POST':
        form = JobsForm(request.POST or None)
        if form.is_valid() and request.POST['item'] != '':
            form.save()
            all_items = Jobs.objects.order_by('completed')
            messages.success(request, request.POST['item']+ ' er blevet tilføjet til din opgave list')
            context = {'all_items': all_items}
            return render(request, 'todo.html', context)
    else:
        all_items =Jobs.objects.order_by('completed')
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
    if request.method == 'POST':
        item = Jobs.objects.get(pk=job_id)
        form = JobsForm(request.POST or None, instance=item)
        if form.is_valid() and request.POST['item'] != '':
            form.save()
            all_items = Jobs.objects.all
            messages.success(request, request.POST['item'] + ' er blevet redigeret i din opgave list')
            return redirect('todo.html')

    else:
        item = Jobs.objects.get(pk=job_id)
        context = {'item': item}
        return render(request, 'edit.html', context)




###########################################################

@method_decorator(login_required, name='dispatch')
class JobsListView(generic.ListView):
    model = models.Jobs
    form_class = forms.JobsForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        return queryset

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        prefetch_related_objects([obj], 'model_hardware__asset')
        return obj

    def delete(request, del_id):
        item = models.Asset.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Udstyr er nu blevet slettet')
        return redirect('asset_app_asset_list')


@method_decorator(login_required, name='dispatch')
class JobsCreateView(generic.CreateView):
    model = models.Jobs
    form_class = forms.JobsForm


@method_decorator(login_required, name='dispatch')
class JobsDetailView(generic.DetailView):
    model = models.Jobs
    form_class = forms.JobsForm


@method_decorator(login_required, name='dispatch')
class JobsUpdateView(generic.UpdateView):
    model = models.Jobs
    form_class = forms.JobsForm
    pk_url_kwarg = "pk"






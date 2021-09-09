from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
    context = super().get_context_data(**kwargs)
    context['to_dos'] = to_do_list_app.models.Jobs.objects.filter(completed=False).order_by('created')
    return render(request, 'home.html', context)


@login_required(login_url='login')
def about(request):
    return render(request, 'about.html', {})
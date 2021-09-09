from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def home(request):
      return render(request, 'home.html', {})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['to_dos'] = to_do_list_app.models.Jobs.objects.filter(completed=False).order_by('created')
        return context

@login_required(login_url='login')
def about(request):
    return render(request, 'about.html', {})
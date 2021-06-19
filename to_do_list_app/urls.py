"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import settings, static
from . import api
from . import views

router = routers.DefaultRouter()
router.register("jobs", api.JobsViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('', views.todo, name='todo'),
    path('delete/<job_id>', views.delete, name='delete'),
    path('cross_off/<job_id>', views.cross_off, name='cross_off'),
    path('uncross/<job_id>', views.uncross, name='uncross'),
    path('edit/<job_id>', views.edit, name='edit'),
    path("to_do_app/to_do/", views.JobsListView.as_view(), name="to_do_app_to_do_list"),
    path("to_do_app/to_do/create/", views.JobsCreateView.as_view(), name="to_do_app_to_do_create"),
    path("to_do_app/to_do/detail/<int:pk>/", views.JobsDetailView.as_view(), name="to_do_app_to_do_detail"),
    path("to_do_app/to_do/update/<int:pk>/", views.JobsUpdateView.as_view(), name="to_do_app_to_do_update"),
    path("to_do_app/to_do/delete/<int:pk>/", views.JobsListView.delete, name="to_do_app_to_do_delete"),
]
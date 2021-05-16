from django.views import generic
from django.shortcuts import render
from . import models
from . import forms


class locationsListView(generic.ListView):
    model = models.Locations
    ordering =['name']
    form_class = forms.locationsForm


class locationsCreateView(generic.CreateView):
    model = models.Locations
    form_class = forms.locationsForm


class locationsDetailView(generic.DetailView):
    model = models.Locations
    form_class = forms.locationsForm


class locationsUpdateView(generic.UpdateView):
    model = models.Locations
    form_class = forms.locationsForm
    pk_url_kwarg = "pk"


class asset_typeListView(generic.ListView):
    model = models.Asset_type
    form_class = forms.asset_typeForm


class asset_typeCreateView(generic.CreateView):
    model = models.Asset_type
    form_class = forms.asset_typeForm


class asset_typeDetailView(generic.DetailView):
    model = models.Asset_type
    form_class = forms.asset_typeForm


class asset_typeUpdateView(generic.UpdateView):
    model = models.Asset_type
    form_class = forms.asset_typeForm
    pk_url_kwarg = "pk"


class loan_assetListView(generic.ListView):
    model = models.Loan_asset
    form_class = forms.loan_assetForm


class loan_assetCreateView(generic.CreateView):
    model = models.Loan_asset
    form_class = forms.loan_assetForm


class loan_assetDetailView(generic.DetailView):
    model = models.Loan_asset
    form_class = forms.loan_assetForm


class loan_assetUpdateView(generic.UpdateView):
    model = models.Loan_asset
    form_class = forms.loan_assetForm
    pk_url_kwarg = "pk"


class roomListView(generic.ListView):
    model = models.Room

    form_class = forms.roomForm



class roomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.roomForm


class roomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.roomForm


class roomUpdateView(generic.UpdateView):
    model = models.Room
    form_class = forms.roomForm
    pk_url_kwarg = "pk"


class assetListView(generic.ListView):
    model = models.Asset
    form_class = forms.assetForm


class assetCreateView(generic.CreateView):
    model = models.Asset
    form_class = forms.assetForm


class assetDetailView(generic.DetailView):
    model = models.Asset
    form_class = forms.assetForm


class assetUpdateView(generic.UpdateView):
    model = models.Asset
    form_class = forms.assetForm
    pk_url_kwarg = "pk"


class loaner_typeListView(generic.ListView):
    model = models.Loaner_type
    form_class = forms.loaner_typeForm


class loaner_typeCreateView(generic.CreateView):
    model = models.Loaner_type
    form_class = forms.loaner_typeForm


class loaner_typeDetailView(generic.DetailView):
    model = models.Loaner_type
    form_class = forms.loaner_typeForm


class loaner_typeUpdateView(generic.UpdateView):
    model = models.Loaner_type
    form_class = forms.loaner_typeForm
    pk_url_kwarg = "pk"


class modelListView(generic.ListView):
    model = models.Model
    form_class = forms.modelForm


class modelCreateView(generic.CreateView):
    model = models.Model
    form_class = forms.modelForm


class modelDetailView(generic.DetailView):
    model = models.Model
    form_class = forms.modelForm


class modelUpdateView(generic.UpdateView):
    model = models.Model
    form_class = forms.modelForm
    pk_url_kwarg = "pk"

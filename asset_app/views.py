from django.views import generic
from . import models
from . import forms

class AssetListView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm


class AssetCreateView(generic.CreateView):
    model = models.Asset
    form_class = forms.AssetForm


class AssetDetailView(generic.DetailView):
    model = models.Asset
    form_class = forms.AssetForm


class AssetUpdateView(generic.UpdateView):
    model = models.Asset
    form_class = forms.AssetForm
    pk_url_kwarg = "pk"



class Asset_typeListView(generic.ListView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm


class Asset_typeCreateView(generic.CreateView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm


class Asset_typeDetailView(generic.DetailView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm


class Asset_typeUpdateView(generic.UpdateView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm
    pk_url_kwarg = "pk"

class BrandListView(generic.ListView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandCreateView(generic.CreateView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandDetailView(generic.DetailView):
    model = models.Brand
    form_class = forms.BrandForm


class BrandUpdateView(generic.UpdateView):
    model = models.Brand
    form_class = forms.BrandForm
    pk_url_kwarg = "pk"

class Loan_assetListView(generic.ListView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm


class Loan_assetCreateView(generic.CreateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm


class Loan_assetDetailView(generic.DetailView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm


class Loan_assetUpdateView(generic.UpdateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm
    pk_url_kwarg = "pk"


class LocationsListView(generic.ListView):
    model = models.Locations
    ordering = ['name']
    form_class = forms.LocationsForm


class LocationsCreateView(generic.CreateView):
    model = models.Locations
    form_class = forms.LocationsForm


class LocationsDetailView(generic.DetailView):
    model = models.Locations
    form_class = forms.LocationsForm


class LocationsUpdateView(generic.UpdateView):
    model = models.Locations
    form_class = forms.LocationsForm
    pk_url_kwarg = "pk"


class Loaner_typeListView(generic.ListView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm


class Loaner_typeCreateView(generic.CreateView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm


class Loaner_typeDetailView(generic.DetailView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm


class Loaner_typeUpdateView(generic.UpdateView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm
    pk_url_kwarg = "pk"


class ModelListView(generic.ListView):
    model = models.Model
    form_class = forms.ModelForm


class ModelCreateView(generic.CreateView):
    model = models.Model
    form_class = forms.ModelForm


class ModelDetailView(generic.DetailView):
    model = models.Model
    form_class = forms.ModelForm


class ModelUpdateView(generic.UpdateView):
    model = models.Model
    form_class = forms.ModelForm
    pk_url_kwarg = "pk"


class RoomListView(generic.ListView):
    model = models.Room
    form_class = forms.RoomForm


class RoomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm


class RoomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


class RoomUpdateView(generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    pk_url_kwarg = "pk"

class Room_typeListView(generic.ListView):
    model = models.Room_type
    form_class = forms.Room_typeForm


class Room_typeCreateView(generic.CreateView):
    model = models.Room_type
    form_class = forms.Room_typeForm


class Room_typeDetailView(generic.DetailView):
    model = models.Room_type
    form_class = forms.Room_typeForm


class Room_typeUpdateView(generic.UpdateView):
    model = models.Room_type
    form_class = forms.Room_typeForm
    pk_url_kwarg = "pk"
from django.shortcuts import redirect
from django.views import generic
from django.db.models import Count, prefetch_related_objects
from django.contrib import messages
import datetime
import os
import urllib.request as Request
from urllib.request import urlopen
from . import models
from . import forms
from django.contrib.auth.decorators import login_required


class AssetListView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm

    
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

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('model_hardware__asset'))
        return qs

    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        prefetch_related_objects([obj], 'model_hardware__asset')
        return obj

    
    def delete(request, del_id):
        item = models.Asset_type.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Udtyrs type er nu blevet slettet')
        return redirect('asset_app_asset_type_list')



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

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        return queryset.annotate(object_count=Count('model_hardware__asset'))

    
    def delete(request, del_id):
        item = models.Brand.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Mærke er nu blevet slettet')
        return redirect('asset_app_brand_list')


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


class Bundle_reservationListView(generic.ListView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('returned','return_date')
        return queryset

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        context["today"] = new_context_entry
        return context

    
    def returned_true(request, res_id):
        item = models.Bundle_reservation.objects.get(pk=res_id)
        item.returned = False
        messages.success(request, 'Noteret udstyret som afleveret')
        item.save()
        return redirect('asset_app_bundle_reservation_list')

    
    def returned_false(request, res_id):
        item = models.Bundle_reservation.objects.get(pk=res_id)
        item.returned = True
        messages.success(request,'Noteret udstyret som ikke afleveret')
        item.save()
        return redirect('asset_app_bundle_reservation_list')


class Bundle_reservationCreateView(generic.CreateView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm


class Bundle_reservationDetailView(generic.DetailView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        context["today"] = new_context_entry
        return context


class Bundle_reservationUpdateView(generic.UpdateView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm
    pk_url_kwarg = "pk"


class Loan_assetListView(generic.ListView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        context["today"] = new_context_entry
        return context

    
    def returned_true(request, res_id):
        item = models.Loan_asset.objects.get(pk=res_id)
        item.returned = False
        messages.success(request, 'Noteret udstyret som afleveret')
        item.save()
        return redirect('asset_app_loan_asset_list')

    
    def returned_false(request, res_id):
        item = models.Loan_asset.objects.get(pk=res_id)
        item.returned = True
        messages.success(request,'Noteret udstyret som ikke afleveret')
        item.save()
        return redirect('asset_app_loan_asset_list')


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
    form_class = forms.LocationsForm

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('room__asset'))
        return qs

    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset.order_by('name'))
        prefetch_related_objects([obj], 'room__asset')
        return obj

    
    def delete(request, del_id):
        item = models.Locations.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Afdeling er nu blevet slettet')
        return redirect('asset_app_locations_list')



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

    
    def delete(request, del_id):
        item = models.Loaner_type.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Låner type er nu blevet slettet')
        return redirect('asset_app_loaner_type_list')


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


class Model_hardwareListView(generic.ListView):
    model = models.Model_hardware
    form_class = forms.ModelForm

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('asset'))
        return qs

    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        prefetch_related_objects([obj], 'model_hardware__asset')
        return obj

    
    def delete(request, del_id):
        item = models.Model_hardware.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Model er nu blevet slettet')
        return redirect('asset_app_model_hardware_list')


class Model_hardwareCreateView(generic.CreateView):
    model = models.Model_hardware
    form_class = forms.ModelForm


class Model_hardwareDetailView(generic.DetailView):
    model = models.Model_hardware
    form_class = forms.ModelForm


class Model_hardwareUpdateView(generic.UpdateView):
    model = models.Model_hardware
    form_class = forms.ModelForm
    pk_url_kwarg = "pk"


class RoomListView(generic.ListView):
    model = models.Room
    form_class = forms.RoomForm

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('asset'))
        return qs

    
    def get_object(self, queryset=None):
        obj = super().object_list(queryset=queryset)
        prefetch_related_objects([obj], 'model_hardware__asset')
        return obj

    
    def delete(request, del_id):
        item = models.Room.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Rum er nu blevet slettet')
        return redirect('asset_app_room_list')

class RoomDashboard(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm

    queryset = super().get_queryset().order_by('name')
    return queryset

class RoomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm


class RoomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


class RoomPDFDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm

    
    def export_pdf_save(request):

        request = Request('https://webtopdf.expeditedaddons.com/?api_key=' + os.environ['WEBTOPDF_API_KEY'] + '&content=127.0.0.1:8000/asset/asset_app/room/detail_pdf/1/&html_width=1024&margin=10&title=My+PDF+Title')

        response_body = urlopen(request).read()
        print(response_body)

    
    def export_pdf_view(request):
        pass



class RoomUpdateView(generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    pk_url_kwarg = "pk"


class Room_typeListView(generic.ListView):
    model = models.Room_type
    form_class = forms.Room_typeForm

    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('room'))
        return qs

    
    def get_object(self, queryset=None):
        obj = super().object_list(queryset=queryset)
        prefetch_related_objects([obj], 'room__asset')
        return obj

    
    def delete(request, del_id):
        item = models.Room_type.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Rum Type er nu blevet slettet')
        return redirect('asset_app_room_type_list')



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
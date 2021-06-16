from django.shortcuts import redirect
from django.views import generic
from django.db.models import Count, prefetch_related_objects, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import urllib.request as Request
from urllib.request import urlopen
import datetime
import os
import to_do_list_app.models
from . import models
from . import forms


@method_decorator(login_required, name='dispatch')
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




@method_decorator(login_required, name='dispatch')
class AssetCreateView(generic.CreateView):
    model = models.Asset
    form_class = forms.AssetForm

@method_decorator(login_required, name='dispatch')
class AssetDetailView(generic.DetailView):
    model = models.Asset
    form_class = forms.AssetForm

@method_decorator(login_required, name='dispatch')
class AssetUpdateView(generic.UpdateView):
    model = models.Asset
    form_class = forms.AssetForm
    pk_url_kwarg = "pk"


@method_decorator(login_required, name='dispatch')
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

    
    def delete(self, request, del_id):
        item = models.Asset_type.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Udtyrs type er nu blevet slettet')
        return redirect('asset_app_asset_type_list')


@method_decorator(login_required, name='dispatch')
class Asset_typeCreateView(generic.CreateView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm

@method_decorator(login_required, name='dispatch')
class Asset_typeDetailView(generic.DetailView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm


@method_decorator(login_required, name='dispatch')
class Asset_typeUpdateView(generic.UpdateView):
    model = models.Asset_type
    form_class = forms.Asset_typeForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class BrandCreateView(generic.CreateView):
    model = models.Brand
    form_class = forms.BrandForm

@method_decorator(login_required, name='dispatch')
class BrandDetailView(generic.DetailView):
    model = models.Brand
    form_class = forms.BrandForm

@method_decorator(login_required, name='dispatch')
class BrandUpdateView(generic.UpdateView):
    model = models.Brand
    form_class = forms.BrandForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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
        messages.success(request, 'Noteret udstyret som ikke afleveret')
        item.save()
        return redirect('asset_app_bundle_reservation_list')

    
    def returned_false(request, res_id):
        item = models.Bundle_reservation.objects.get(pk=res_id)
        item.returned = True
        messages.success(request,'Noteret udstyret som afleveret')
        item.save()
        return redirect('asset_app_bundle_reservation_list')

@method_decorator(login_required, name='dispatch')
class Bundle_reservationCreateView(generic.CreateView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm

@method_decorator(login_required, name='dispatch')
class Bundle_reservationDetailView(generic.DetailView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        context["today"] = new_context_entry
        return context

@method_decorator(login_required, name='dispatch')
class Bundle_reservationUpdateView(generic.UpdateView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm
    pk_url_kwarg = "pk"

class Dashboard(generic.TemplateView):
    template_name = "asset_app/dashboard.html"

    def get_queryset(self):
        queryset = super().get_queryset().order_by('last_inspected')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_entry_today = datetime.date.today()
        context_entry_overdue = datetime.date.today() - datetime.timedelta(days=90)
        context_entry_inspection_time = datetime.date.today() - datetime.timedelta(days=76)
        context['rooms'] = models.Room.objects.exclude(room_type__name='Skole').exclude(room_type__name='Afdeling').order_by('last_inspected', 'location', 'name')
        context['bundelReservations'] = models.Bundle_reservation.objects.order_by('return_date')
        context['loan_assets'] = models.Loan_asset.objects.order_by('return_date')
        context['routinelogs'] = models.RoutineLog.objects.all().order_by('routine__name','-date').distinct('routine__name')
        context['to_dos'] = to_do_list_app.models.Jobs.objects.all()
        context['routines'] = models.Routines.objects.all().order_by('name')
        context["today"] = context_entry_today
        context["overdue"] = context_entry_overdue
        context["inspection_time"] = context_entry_inspection_time
        return context

@method_decorator(login_required, name='dispatch')
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

    def get_queryset(self):
        queryset = super().get_queryset().order_by('loaner_name','asset')
        return queryset

@method_decorator(login_required, name='dispatch')
class Loan_assetCreateView(generic.CreateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

@method_decorator(login_required, name='dispatch')
class Loan_assetDetailView(generic.DetailView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

@method_decorator(login_required, name='dispatch')
class Loan_assetUpdateView(generic.UpdateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class LocationsCreateView(generic.CreateView):
    model = models.Locations
    form_class = forms.LocationsForm

@method_decorator(login_required, name='dispatch')
class LocationsDetailView(generic.DetailView):
    model = models.Locations
    form_class = forms.LocationsForm

@method_decorator(login_required, name='dispatch')
class LocationsUpdateView(generic.UpdateView):
    model = models.Locations
    form_class = forms.LocationsForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class Loaner_typeListView(generic.ListView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm

    
    def delete(request, del_id):
        item = models.Loaner_type.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Låner type er nu blevet slettet')
        return redirect('asset_app_loaner_type_list')

@method_decorator(login_required, name='dispatch')
class Loaner_typeCreateView(generic.CreateView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm

@method_decorator(login_required, name='dispatch')
class Loaner_typeDetailView(generic.DetailView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm

@method_decorator(login_required, name='dispatch')
class Loaner_typeUpdateView(generic.UpdateView):
    model = models.Loaner_type
    form_class = forms.Loaner_typeForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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

@method_decorator(login_required, name='dispatch')
class Model_hardwareCreateView(generic.CreateView):
    model = models.Model_hardware
    form_class = forms.ModelForm

@method_decorator(login_required, name='dispatch')
class Model_hardwareDetailView(generic.DetailView):
    model = models.Model_hardware
    form_class = forms.ModelForm

@method_decorator(login_required, name='dispatch')
class Model_hardwareUpdateView(generic.UpdateView):
    model = models.Model_hardware
    form_class = forms.ModelForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class One2OneInfoListView(generic.ListView):
    model = models.One2OneInfo
    form_class = forms.One2OneInfoForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        qs = queryset.annotate(object_count=Count('one2oneInfoLog'))
        return qs

    def completed_false(request, res_id):
        item = models.Bundle_reservation.objects.get(pk=one_two_one_id)
        item.returned = False
        messages.success(request, 'Opgaven er ikke noteret som løst')
        item.save()
        return redirect('asset_app_one2one_list')

    def completed_true(request, res_id):
        item = models.Bundle_reservation.objects.get(pk=one_two_one_id)
        item.returned = True
        messages.success(request, 'Opgaven er noteret som løst')
        item.save()
        return redirect('asset_app_one2one_list')

    def delete(request, del_id):
        item = models.One2OneInfo.objects.get(pk=del_id)
        item.delete()
        messages.success(request, '1-til-1 opgave er nu blevet slettet')
        return redirect('asset_app_one2one_list')

@method_decorator(login_required, name='dispatch')
class One2OneInfoCreateView(generic.CreateView):
    model = models.One2OneInfo
    form_class = forms.One2OneInfoForm

@method_decorator(login_required, name='dispatch')
class One2OneInfoDetailView(generic.DetailView):
    model = models.One2OneInfo
    form_class = forms.One2OneInfoForm

@method_decorator(login_required, name='dispatch')
class One2OneInfoUpdateView(generic.UpdateView):
    model = models.One2OneInfo
    form_class = forms.One2OneInfoForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class One2OneInfoLogListView(generic.ListView):
    model = models.One2OneInfoLog
    form_class = forms.One2OneInfoLogForm

    def delete(request, del_id):
        item = models.One2OneInfoLog.objects.get(pk=del_id)
        item.delete()
        messages.success(request, '1-til-1 opgave er nu blevet slettet')
        return redirect('asset_app_one2one_log_list')

@method_decorator(login_required, name='dispatch')
class One2OneInfoLogCreateView(generic.CreateView):
    model = models.One2OneInfoLog
    form_class = forms.One2OneInfoLogForm

@method_decorator(login_required, name='dispatch')
class One2OneInfoLogDetailView(generic.DetailView):
    model = models.One2OneInfoLog
    form_class = forms.One2OneInfoLogForm

@method_decorator(login_required, name='dispatch')
class One2OneInfoLogUpdateView(generic.UpdateView):
    model = models.One2OneInfoLog
    form_class = forms.One2OneInfoLogForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class RoomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm

@method_decorator(login_required, name='dispatch')
class RoomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


class RoomPDFDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


    def export_pdf_save(request):

        request = Request('https://webtopdf.expeditedaddons.com/?api_key=' + os.environ['WEBTOPDF_API_KEY'] + '&content=/asset/asset_app/room/detail_pdf/1/&html_width=1024&margin=10&title=My+PDF+Title')

        response_body = urlopen(request).read()
        print(response_body)

    
    def export_pdf_view(request):
        pass


@method_decorator(login_required, name='dispatch')
class RoomUpdateView(generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
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


@method_decorator(login_required, name='dispatch')
class Room_typeCreateView(generic.CreateView):
    model = models.Room_type
    form_class = forms.Room_typeForm

@method_decorator(login_required, name='dispatch')
class Room_typeDetailView(generic.DetailView):
    model = models.Room_type
    form_class = forms.Room_typeForm

@method_decorator(login_required, name='dispatch')
class Room_typeUpdateView(generic.UpdateView):
    model = models.Room_type
    form_class = forms.Room_typeForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class RoutinesListView(generic.ListView):
    model = models.Routines
    form_class = forms.RoutinesForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('name')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_entry_today = datetime.date.today()
        context_entry_overdue = datetime.date.today() - datetime.timedelta(days=2)
        context['routinelogs'] = models.RoutineLog.objects.all().order_by('routine__name','-date').distinct('routine__name')
        context["today"] = context_entry_today
        context["overdue"] = context_entry_overdue
        return context

@method_decorator(login_required, name='dispatch')
class RoutinesCreateView(generic.CreateView):
    model = models.Routines
    form_class = forms.RoutinesForm

@method_decorator(login_required, name='dispatch')
class RoutinesDetailView(generic.DetailView):
    model = models.Routines
    form_class = forms.RoutinesForm

@method_decorator(login_required, name='dispatch')
class RoutinesUpdateView(generic.UpdateView):
    model = models.Routines
    form_class = forms.RoutinesForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class RoutineLogListView(generic.ListView):
    model = models.RoutineLog
    form_class = forms.RoutineLogForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-date')
        return queryset

@method_decorator(login_required, name='dispatch')
class RoutineLogCreateView(generic.CreateView):
    model = models.RoutineLog
    form_class = forms.RoutineLogForm

@method_decorator(login_required, name='dispatch')
class RoutineLogDetailView(generic.DetailView):
    model = models.RoutineLog
    form_class = forms.RoutineLogForm

@method_decorator(login_required, name='dispatch')
class RoutineLogUpdateView(generic.UpdateView):
    model = models.RoutineLog
    form_class = forms.RoutineLogForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class SearchView(generic.TemplateView):
    template_name = "asset_app/search.html"

    def post(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        searched = self.request.POST.get('searched')
        context['searched'] = searched
        context_entry_today = datetime.date.today()
        context_entry_overdue = datetime.date.today() - datetime.timedelta(days=90)
        context_entry_inspection_time = datetime.date.today() - datetime.timedelta(days=76)
        context['assets'] = models.Asset.objects.filter(Q(name__icontains=searched) | Q(serial__icontains=searched) | Q(mac_address__icontains=searched) | Q(ip__icontains=searched) | Q(model_hardware__name__icontains=searched) | Q(room__name__icontains=searched)).order_by('name')
        context['rooms'] = models.Room.objects.filter(name__contains=searched).order_by('last_inspected', 'location', 'name')
        context['bundelReservations'] = models.Bundle_reservation.objects.filter(loaner_name__contains=searched).order_by('return_date')
        context['loan_assets'] = models.Loan_asset.objects.filter(loaner_name__contains=searched).order_by('return_date')
        context['to_dos'] = to_do_list_app.models.Jobs.objects.filter(item__contains=searched)
        context['today'] = context_entry_today
        context['overdue'] = context_entry_overdue
        context['inspection_time'] = context_entry_inspection_time
        return self.render_to_response(context)




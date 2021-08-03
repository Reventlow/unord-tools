from django.shortcuts import redirect, render
from django.views import generic
from django.db.models import Count, prefetch_related_objects, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.functions import Lower
from django.utils.translation import ugettext
import csv
from django.http import HttpResponse
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
import urllib.request as Request
from urllib.request import urlopen
import datetime
import os
import to_do_list_app.models
from . import models
from . import forms
from io import StringIO, BytesIO
import xlsxwriter


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
class AssetCaseListView(generic.ListView):
    model = models.AssetCase
    form_class = forms.AssetCaseForm

    def set_solved_true(request, asset_case_id):
        item = models.AssetCase.objects.get(pk=asset_case_id)
        item.solved = True
        messages.success(request, 'Sagen er noteret som afsluttede')
        item.save()
        return redirect('asset_app_AssetCase_list')

    def set_solved_false(request, asset_case_id):
        item = models.Assetcase.objects.get(pk=asset_case_id)
        item.solved = False
        messages.success(request, 'Sag er noteret som ikke løst')
        item.save()
        return redirect('asset_app_AssetCase_list')

    def get_queryset(self):
        queryset = super().get_queryset().order_by('solved', 'created')
        return queryset


@method_decorator(login_required, name='dispatch')
class AssetCaseCreateView(generic.CreateView):
    model = models.AssetCase
    form_class = forms.AssetCaseForm


@method_decorator(login_required, name='dispatch')
class AssetCaseDetailView(generic.DetailView):
    model = models.AssetCase
    form_class = forms.AssetCaseForm


@method_decorator(login_required, name='dispatch')
class AssetCaseUpdateView(generic.UpdateView):
    model = models.AssetCase
    form_class = forms.AssetCaseForm
    pk_url_kwarg = "pk"


@method_decorator(login_required, name='dispatch')
class AssetLogListView(generic.ListView):
    model = models.AssetLog
    form_class = forms.AssetLogForm

    def delete(request, del_id):
        item = models.AssetLog.get(pk=del_id)
        item.delete()
        messages.success(request, 'Sags notat er slettet')
        return redirect('asset_app_AssetLog_list')



@method_decorator(login_required, name='dispatch')
class AssetLogCreateView(generic.CreateView):
    model = models.AssetLog
    form_class = forms.AssetLogForm


@method_decorator(login_required, name='dispatch')
class AssetLogDetailView(generic.DetailView):
    model = models.AssetLog
    form_class = forms.AssetLogForm


@method_decorator(login_required, name='dispatch')
class AssetLogUpdateView(generic.UpdateView):
    model = models.AssetLog
    form_class = forms.AssetLogForm
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
        queryset = super().get_queryset().order_by('returned', 'return_date')
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
        messages.success(request, 'Noteret udstyret som afleveret')
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
        context['rooms'] = models.Room.objects.exclude(room_type__name='Skole').exclude(
            room_type__name='Afdeling').exclude(last_inspected=None).exclude(last_inspected__gt=context_entry_inspection_time).order_by('last_inspected', 'location', 'name')
        context['assetCases'] = models.AssetCase.objects.exclude(solved='True').order_by('created')
        context['bundelReservations'] = models.Bundle_reservation.objects.exclude(return_date__gt=datetime.date.today()).filter(returned=False).order_by('return_date')
        context['loan_assets'] = models.Loan_asset.objects.exclude(return_date__gt=datetime.date.today()).filter(returned=False).order_by('return_date')
        context['routinelogs'] = models.RoutineLog.objects.all().order_by('routine__name', '-date').distinct(
            'routine__name')
        context['one2ones'] = models.One2OneInfo.objects.filter(completed=False).annotate(
            object_count=Count('one2oneinfolog')).order_by('name')
        context['to_dos'] = to_do_list_app.models.Jobs.objects.filter(completed=False).order_by('created')
        context['routines'] = models.Routines.objects.all().order_by('name')
        context["today"] = context_entry_today
        context["overdue"] = context_entry_overdue
        context["inspection_time"] = context_entry_inspection_time
        return context


@method_decorator(login_required, name='dispatch')
class ExternalServiceListView(generic.ListView):
    model = models.ExternalService
    form_class = forms.ExternalServiceForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('company_name')
        qs = queryset.annotate(object_count=Count('externalservicecontact'))
        return qs

    def delete(request, del_id):
        item = models.ExternalService.get(pk=del_id)
        item.delete()
        messages.success(request, 'Firmaet er nu blevet slettet')
        return redirect('asset_app_ExternalService_list')


@method_decorator(login_required, name='dispatch')
class ExternalServiceCreateView(generic.CreateView):
    model = models.ExternalService
    form_class = forms.ExternalServiceForm


@method_decorator(login_required, name='dispatch')
class ExternalServiceDetailView(generic.DetailView):
    model = models.ExternalService
    form_class = forms.ExternalServiceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = self.object.externalservicecontact_set.order_by('name')
        return context


@method_decorator(login_required, name='dispatch')
class ExternalServiceUpdateView(generic.UpdateView):
    model = models.ExternalService
    form_class = forms.ExternalServiceForm
    pk_url_kwarg = "pk"


@method_decorator(login_required, name='dispatch')
class ExternalServiceContactListView(generic.ListView):
    model = models.ExternalServiceContact
    form_class = forms.ExternalServiceContactForm

    def delete(request, del_id):
        item = models.ExternalServiceContact.get(pk=del_id)
        item.delete()
        messages.success(request, 'Kontakt er nu blevet slettet')
        return redirect('asset_app_ExternalService_list')


@method_decorator(login_required, name='dispatch')
class ExternalServiceContactCreateView(generic.CreateView):
    model = models.ExternalServiceContact
    form_class = forms.ExternalServiceContactForm


@method_decorator(login_required, name='dispatch')
class ExternalServiceContactDetailView(generic.DetailView):
    model = models.ExternalServiceContact
    form_class = forms.ExternalServiceContactForm


@method_decorator(login_required, name='dispatch')
class ExternalServiceContactUpdateView(generic.UpdateView):
    model = models.ExternalServiceContact
    form_class = forms.ExternalServiceContactForm
    pk_url_kwarg = "pk"


@method_decorator(login_required, name='dispatch')
class ExternalServicePositionListView(generic.ListView):
    model = models.ExternalServicePosition
    form_class = forms.ExternalServicePositionForm

    def delete(request, del_id):
        item = models.ExternalServicePosition.get(pk=del_id)
        item.delete()
        messages.success(request, 'Stilling er nu blevet slettet')
        return redirect('asset_app_ExternalServicePosition_list')


@method_decorator(login_required, name='dispatch')
class ExternalServicePositionCreateView(generic.CreateView):
    model = models.ExternalServicePosition
    form_class = forms.ExternalServicePositionForm


@method_decorator(login_required, name='dispatch')
class ExternalServicePositionDetailView(generic.DetailView):
    model = models.ExternalServicePosition
    form_class = forms.ExternalServicePositionForm


@method_decorator(login_required, name='dispatch')
class ExternalServicePositionUpdateView(generic.UpdateView):
    model = models.ExternalServicePosition
    form_class = forms.ExternalServicePositionForm
    pk_url_kwarg = "pk"


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
        messages.success(request, 'Noteret udstyret som ikke afleveret')
        item.save()
        return redirect('asset_app_loan_asset_list')

    def get_queryset(self):
        queryset = super().get_queryset().order_by('returned', 'loaner_name', 'asset')
        return queryset


@method_decorator(login_required, name='dispatch')
class Loan_assetCreateView(generic.CreateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('asset__model_hardware__asset_type', 'asset.name')
        return queryset


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
class LocationLaptopListView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm



    def get_queryset(self):
        location = self.kwargs['location']
        queryset = super().get_queryset().filter(room__location__name=location).filter(model_hardware__asset_type__name="Bærebar").order_by('name')
        return queryset


    def get(self, request, location):

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Bærebar på "+location)

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        worksheet_s.write(2, 1, ugettext("Bærebar"), header)
        worksheet_s.write(2, 2, ugettext("Placering"), header)
        worksheet_s.write(2, 3, ugettext("Mærke og model"), header)
        worksheet_s.write(2, 4, ugettext("Serienummer"), header)
        worksheet_s.write(2, 5, ugettext("Må udlånes"), header)

        queryset = super().get_queryset().filter(room__location__name=location).filter(model_hardware__asset_type__name="Bærebar").order_by('name')

        for idx, data in enumerate(queryset):
            row = 3 + idx
            worksheet_s.write_number(row, 0, idx + 1)
            worksheet_s.write_string(row, 1, data.name)
            worksheet_s.write_string(row, 2, data.room.name+'-POA')
            worksheet_s.write_string(row, 3, data.model_hardware.name)
            worksheet_s.write_string(row, 4, data.serial)
            worksheet_s.write_boolean(row, 5, data.may_be_loaned)
            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 15)
        worksheet_s.set_column('E:E', 30)
        worksheet_s.set_column('F:F', 10)


        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Bærebar-´'+location+'-'+str(datetime.date.today())+'.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response





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
        qs = queryset.annotate(object_count=Count('one2oneinfolog'))
        return qs

    def completed_false(request, one_two_one_id):
        item = models.Bundle_reservation.objects.get(pk=one_two_one_id)
        item.returned = False
        messages.success(request, 'Opgaven er ikke noteret som løst')
        item.save()
        return redirect('asset_app_one2one_list')

    def completed_true(request, one_two_one_id):
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

    def export_csv(request, pk):
        response = HttpResponse(content_type='text/csv')

        writer = csv.writer(response)
        writer.writerow(['Brugernavn', 'Afdeling', 'Tidspunkt for gennemgang UTC'])

        for user in models.One2OneInfoLog.objects.filter(one_2_one_info=pk).values_list(Lower('name'), 'location',
                                                                                        'created').order_by('-created'):
            writer.writerow(user)

        response['Content-Disposition'] = 'attachment';
        filename = '1-til-1-opgave.csv'
        return response


@method_decorator(login_required, name='dispatch')
class One2OneInfoUpdateView(generic.UpdateView):
    model = models.One2OneInfo
    form_class = forms.One2OneInfoForm
    pk_url_kwarg = "pk"


@method_decorator(login_required, name='dispatch')
class One2OneInfoLogListView(generic.ListView):
    model = models.One2OneInfoLog
    form_class = forms.One2OneInfoLogForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created')
        return queryset

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
        queryset = super().get_queryset().order_by('location', 'name')
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

@method_decorator(login_required, name='dispatch')
class RoomPDFDetailView(PDFTemplateResponseMixin, generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm
    template_name = 'asset_app/room_detail_to-pdf.html'




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

    def get_queryset(self):
        queryset = super().get_queryset().order_by('asset_type.name', 'name')
        return queryset


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
        context['routinelogs'] = models.RoutineLog.objects.all().order_by('routine__name', '-date').distinct(
            'routine__name')
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
        context['assets'] = models.Asset.objects.filter(
            Q(name__icontains=searched) | Q(serial__icontains=searched) | Q(mac_address__icontains=searched) | Q(
                ip__icontains=searched) | Q(model_hardware__name__icontains=searched) | Q(
                room__name__icontains=searched)).order_by('name')
        context['rooms'] = models.Room.objects.filter(name__icontains=searched).order_by('last_inspected', 'location',
                                                                                         'name')
        context['bundelReservations'] = models.Bundle_reservation.objects.filter(
            loaner_name__icontains=searched).order_by('return_date')
        context['loan_assets'] = models.Loan_asset.objects.filter(loaner_name__icontains=searched).order_by(
            'return_date')
        context['to_dos'] = to_do_list_app.models.Jobs.objects.filter(item__icontains=searched)
        context['today'] = context_entry_today
        context['overdue'] = context_entry_overdue
        context['inspection_time'] = context_entry_inspection_time
        return self.render_to_response(context)


@method_decorator(login_required, name='dispatch')
class SeverityLevelListView(generic.ListView):
    model = models.SeverityLevel
    form_class = forms.SeverityLevelForm

    def delete(request, del_id):
        item = models.SeverityLevel.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Påvirknings grad er nu blevet slettet')
        return redirect('asset_app_SeverityLevel_list')


@method_decorator(login_required, name='dispatch')
class SeverityLevelCreateView(generic.CreateView):
    model = models.SeverityLevel
    form_class = forms.SeverityLevelForm


@method_decorator(login_required, name='dispatch')
class SeverityLevelDetailView(generic.DetailView):
    model = models.SeverityLevel
    form_class = forms.SeverityLevelForm


@method_decorator(login_required, name='dispatch')
class SeverityLevelUpdateView(generic.UpdateView):
    model = models.SeverityLevel
    form_class = forms.SeverityLevelForm
    pk_url_kwarg = "pk"



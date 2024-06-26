import requests
from django.shortcuts import redirect, render
from django.views import generic
from django.db.models import Count, prefetch_related_objects, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models.functions import Lower
from django.utils.translation import ugettext
from django.db.models.signals import post_save
from django.dispatch import receiver
import csv
from django.http import HttpResponse, HttpResponseRedirect
from easy_pdf.views import PDFTemplateView, PDFTemplateResponseMixin
import datetime
from datetime import date
import os
import to_do_list_app.models
from . import models
from . import forms
from io import StringIO, BytesIO
from urllib.request import urlopen
import xlsxwriter
from .tools import smsButtonLateReturn, dateWeekday, smsButtonReturnReminder
from .serializers import AssetSerializer, Loan_assetSerializer
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi




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

    def delete(request, pk):
        item = models.Asset.objects.get(pk=pk)
        item.delete()
        messages.success(request, 'Udstyr er nu blevet slettet')
        return redirect('asset_app_asset_list', location='all')


@method_decorator(login_required, name='dispatch')
class AssetCreateView(generic.CreateView):
    model = models.Asset
    form_class = forms.AssetForm
    location_url_kwarg = "all"



@method_decorator(login_required, name='dispatch')
class AssetDetailView(generic.DetailView):
    model = models.Asset
    form_class = forms.AssetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        context["today"] = new_context_entry

        pk = self.kwargs['pk']
        context["object_list"] = models.Loan_asset.objects.filter(asset_id=pk).order_by('returned', 'return_date', 'loaner_name', 'asset')


        return context

    def returned_true(request, pk):
        item = models.Loan_asset.objects.get(pk=pk)
        item.returned = False
        asset_id = item.asset.id
        messages.success(request, 'Noteret udstyret som ikke afleveret')
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = True
        item.save()
        return redirect('asset_app_asset_detail', pk=asset_id)

    def returned_false(request, pk):
        item = models.Loan_asset.objects.get(pk=pk)
        item.returned = True
        asset_id = item.asset.id
        messages.success(request, 'Noteret udstyret som afleveret')
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = False
        item.save()
        return redirect('asset_app_asset_detail', pk=asset_id)

    def addMonthToCurrentDate(request, pk):
        item = models.Loan_asset.objects.get(pk=pk)
        item.return_date = datetime.date.today() + datetime.timedelta(days=30)
        weekno = item.return_date.weekday()
        if weekno == 5:
            item.return_date = item.return_date + datetime.timedelta(days=2)
        elif weekno == 6:  # 5 Sat, 6 Sun
            item.return_date = item.return_date + datetime.timedelta(days=1)
        asset_id = item.asset.id
        item.save()
        messages.success(request, 'Udvidet låne aftalen med en månede fra dags dato.')
        return redirect('asset_app_asset_detail', pk=asset_id)


@method_decorator(login_required, name='dispatch')
class AssetUpdateView(generic.UpdateView):
    model = models.Asset
    form_class = forms.AssetForm
    pk_url_kwarg = "pk"
    location_url_kwarg = "all"


class AssetViewAPI(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Asset.objects.all()
    serializer_class = AssetSerializer

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
class Asset_typeDetailExcelView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm

    def get(self, request, pk):

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Udstyr")

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                         'font_color': '#9C0006'})

        worksheet_s.write(2, 1, ugettext("Udstyrs navn"), header)
        worksheet_s.write(2, 2, ugettext("Serienummer"), header)
        worksheet_s.write(2, 3, ugettext("Placering"), header)
        worksheet_s.write(2, 4, ugettext("Model"), header)
        worksheet_s.write(2, 5, ugettext("Mærke"), header)
        worksheet_s.write(2, 6, ugettext("Udstyr type"), header)
        worksheet_s.write(2, 7, ugettext("Må udlånes"), header)
        worksheet_s.write(2, 8, ugettext("Meldt savnede"), header)

        queryset = models.Asset.objects.filter(model_hardware__asset_type_id=pk).order_by('name')

        for idx, data in enumerate(queryset):
            row = 3 + idx

            if data.missing:

                worksheet_s.write_number(row, 0, idx + 1, formatRed)
                worksheet_s.write_string(row, 1, data.name, formatRed)
                worksheet_s.write_string(row, 2, data.serial, formatRed)
                worksheet_s.write_string(row, 3,
                                         data.room.name + " :: " + data.room.location.name + " :: " + data.room.room_type.name,
                                         formatRed)
                worksheet_s.write_string(row, 4, data.model_hardware.name, formatRed)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name, formatRed)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name, formatRed)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned, formatRed)
                worksheet_s.write_boolean(row, 8, data.missing, formatRed)
            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.name)
                worksheet_s.write_string(row, 2, data.serial)
                worksheet_s.write_string(row, 3,
                                         data.room.name + " :: " + data.room.location.name + " :: " + data.room.room_type.name)
                worksheet_s.write_string(row, 4, data.model_hardware.name)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned)
                worksheet_s.write_boolean(row, 8, data.missing)

            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 40)
        worksheet_s.set_column('E:E', 25)
        worksheet_s.set_column('F:F', 30)
        worksheet_s.set_column('G:G', 35)
        worksheet_s.set_column('H:H', 15)
        worksheet_s.set_column('I:I', 15)
        worksheet_s.set_column('J:J', 15)

        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.

        filename = 'Udstyr-' + str(datetime.date.today()) + '.xlsx'

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


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
class BrandDetailExcelView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm

    def get(self, request, pk):

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Udstyr")

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                         'font_color': '#9C0006'})

        worksheet_s.write(2, 1, ugettext("Udstyrs navn"), header)
        worksheet_s.write(2, 2, ugettext("Serienummer"), header)
        worksheet_s.write(2, 3, ugettext("Placering"), header)
        worksheet_s.write(2, 4, ugettext("Model"), header)
        worksheet_s.write(2, 5, ugettext("Mærke"), header)
        worksheet_s.write(2, 6, ugettext("Udstyr type"), header)
        worksheet_s.write(2, 7, ugettext("Må udlånes"), header)
        worksheet_s.write(2, 8, ugettext("Meldt savnede"), header)

        queryset = models.Asset.objects.filter(model_hardware__brand_id=pk).order_by('name')

        for idx, data in enumerate(queryset):
            row = 3 + idx

            if data.missing:

                worksheet_s.write_number(row, 0, idx + 1, formatRed)
                worksheet_s.write_string(row, 1, data.name, formatRed)
                worksheet_s.write_string(row, 2, data.serial, formatRed)
                worksheet_s.write_string(row, 3,
                                         data.room.name + " :: " + data.room.location.name + " :: " + data.room.room_type.name,
                                         formatRed)
                worksheet_s.write_string(row, 4, data.model_hardware.name, formatRed)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name, formatRed)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name, formatRed)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned, formatRed)
                worksheet_s.write_boolean(row, 8, data.missing, formatRed)
            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.name)
                worksheet_s.write_string(row, 2, data.serial)
                worksheet_s.write_string(row, 3,
                                         data.room.name + " :: " + data.room.location.name + " :: " + data.room.room_type.name)
                worksheet_s.write_string(row, 4, data.model_hardware.name)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned)
                worksheet_s.write_boolean(row, 8, data.missing)

            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 40)
        worksheet_s.set_column('E:E', 25)
        worksheet_s.set_column('F:F', 30)
        worksheet_s.set_column('G:G', 35)
        worksheet_s.set_column('H:H', 15)
        worksheet_s.set_column('I:I', 15)
        worksheet_s.set_column('J:J', 15)

        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.

        filename = 'Udstyr-' + str(datetime.date.today()) + '.xlsx'

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


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
class Bundle_reservationListExcelView(generic.DetailView):
    model = models.Bundle_reservation
    form_class = forms.Bundle_reservationForm


    def get(self, request):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Sæt udlån")

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatDate = workbook.add_format({'num_format': 'dd/mm/yy'})

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})

        formatGreen = workbook.add_format({'bg_color': '#5A916E',
                                         'font_color': '#FFFFFF'})

        thisColumn = 1
        thisRow = 2

        worksheet_s.write(thisRow, 1, ugettext("Udlåner"), header)
        worksheet_s.write(thisRow, 2, ugettext("Udlånt fra"), header)
        worksheet_s.write(thisRow, 3, ugettext("Antal"), header)
        worksheet_s.write(thisRow, 4, ugettext("Udstyrs type"), header)
        worksheet_s.write(thisRow, 5, ugettext("Serie"), header)
        worksheet_s.write(thisRow, 6, ugettext("Reseveret fra"), header)
        worksheet_s.write(thisRow, 7, ugettext("Retuners"), header)
        worksheet_s.write(thisRow, 8, ugettext("Retuneret"), header)




        thisRow = thisRow +1
        queryset = models.Bundle_reservation.objects.all().order_by('returned', 'loaner_name')

        for idx, data in enumerate(queryset):
            row = thisRow + idx

            if data.return_date > datetime.date.today() and data.returned == False:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.loaner_name)
                worksheet_s.write_string(row, 2, data.location.name)
                worksheet_s.write_number(row, 3, data.amount)
                worksheet_s.write_string(row, 5, data.series)
                worksheet_s.write_string(row, 5, data.asset_type.name)
                worksheet_s.write_string(row, 6, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'))
                worksheet_s.write_string(row, 7, datetime.datetime.strptime(str(data.return_date), '%Y-%m-%d').strftime('%d/%m/%Y'))
                if data.returned == True:
                    returnedValue = "Ja"
                else:
                    returnedValue = "Nej"
                worksheet_s.write_string(row, 8, returnedValue)


            elif data.return_date < datetime.date.today() and data.returned == False:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.loaner_name, formatRed)
                worksheet_s.write_string(row, 2, data.location.name, formatRed)
                worksheet_s.write_number(row, 3, data.amount, formatRed)
                worksheet_s.write_string(row, 4, data.asset_type.name, formatRed)
                worksheet_s.write_string(row, 5, data.series, formatRed)
                worksheet_s.write_string(row, 6, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatRed)
                worksheet_s.write_string(row, 7, datetime.datetime.strptime(str(data.return_date),  '%Y-%m-%d').strftime('%d/%m/%Y'), formatRed)
                if data.returned == True:
                    returnedValue = "Ja"
                else:
                    returnedValue = "Nej"
                worksheet_s.write_string(row, 8, returnedValue, formatRed)

            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.loaner_name, formatGreen)
                worksheet_s.write_string(row, 2, data.location.name, formatGreen)
                worksheet_s.write_number(row, 3, data.amount, formatGreen)
                worksheet_s.write_string(row, 4, data.asset_type.name, formatGreen)
                worksheet_s.write_string(row, 5, data.series, formatGreen)
                worksheet_s.write_string(row, 6, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatGreen)
                worksheet_s.write_string(row, 7, datetime.datetime.strptime(str(data.return_date),  '%Y-%m-%d').strftime('%d/%m/%Y'), formatGreen)
                if data.returned == True:
                    returnedValue = "Ja"
                else:
                    returnedValue = "Nej"
                worksheet_s.write_string(row, 8, returnedValue, formatGreen)


            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 15)
        worksheet_s.set_column('E:E', 15)
        worksheet_s.set_column('F:F', 30)
        worksheet_s.set_column('G:G', 30)
        worksheet_s.set_column('H:H', 20)
        worksheet_s.set_column('H:H', 30)
        worksheet_s.set_column('I:I', 15)



        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Sæt_udlån_' + str(datetime.date.today()) + '.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response

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
        context['loan_assets'] = models.Loan_asset.objects.exclude(return_date__gt=datetime.date.today()).exclude(location__name="MIL").filter(returned=False).order_by('return_date')
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


class DashboardMonthLoanOverview(generic.TemplateView):
    template_name = "asset_app/dashboardMonthLoanOverview.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

########Table head
        htmlTable = '<table class="table"><tr class="table-dark"><td></td>'

        for location in models.Locations.objects.exclude(name='U/NORD').order_by('name'):
            htmlTable = htmlTable + '<td><div style="text-align: center;">' + location.name + '</div></td>'

########Total sum of loans
        htmlTable = htmlTable + '</tr><tr class="table-info">'

        htmlTable = htmlTable + "<td>Udlånt nuværende tidspunkt total</td>"
        for location in models.Locations.objects.exclude(name='U/NORD').order_by('name'):
            criterionLocation = Q(location__name=location.name)
            criterionReturnNot = Q(returned=False)
            thisQuerysetLocationTotal = models.Loan_asset.objects.filter(criterionLocation & criterionReturnNot).count()
            if thisQuerysetLocationTotal > 0:
                htmlTable = htmlTable + '<td><div style="text-align: center;">' + str(
                    thisQuerysetLocationTotal) + '</a></div></td>'
            else:
                htmlTable = htmlTable + '<td><div style="text-align: center;">0</div></td>'

        ########Loan that are to be retured before today
        htmlTable = htmlTable + '</tr><tr class="table-danger">'

        thisQueryDate = datetime.date.today()

        htmlTable = htmlTable + "<td> Udlån der ikke er blevet afleveret til tiden (dags udlån / periode udlån / total)</td>"

        for location in models.Locations.objects.exclude(name='U/NORD').order_by('name'):
            criterionLaonDate = Q(loan_date=thisQueryDate)
            criterionLoanDateNot = ~Q(loan_date=thisQueryDate)
            criterionReturnDate = Q(return_date__lt=thisQueryDate)
            criterionLocation = Q(location__name=location.name)
            criterionReturnNot = Q(returned=False)

            thisQuerysetLocationLoanDay = models.Loan_asset.objects.filter(criterionLaonDate & criterionReturnDate & criterionLocation & criterionReturnNot).count()
            thisQuerysetLocationLoanPeriod = models.Loan_asset.objects.filter(criterionLocation & criterionReturnNot & criterionLoanDateNot & criterionReturnDate).count()
            thisQuerysetLocationTotal = models.Loan_asset.objects.filter(criterionReturnDate & criterionLocation & criterionReturnNot).count()

            if thisQuerysetLocationLoanDay > 0 or thisQuerysetLocationLoanPeriod > 0 or thisQuerysetLocationTotal > 0:
                thisLink = '<a href="filter/'+location.name+'/'+str(thisQueryDate)+'/'+str(False)+'/late/">'

                htmlTable = htmlTable + '<td><div style="text-align: center;">' + thisLink + str(
                    thisQuerysetLocationLoanDay) + '/' + str(thisQuerysetLocationLoanPeriod) + '/' + str(
                    thisQuerysetLocationTotal) + '</a></div></td>'
            else:
                htmlTable = htmlTable + '<td><div style="text-align: center;">' + str(
                    thisQuerysetLocationLoanDay) + '/' + str(thisQuerysetLocationLoanPeriod) + '/' + str(
                    thisQuerysetLocationTotal) + '</div></td>'

########Loan that are to be retured today
        htmlTable = htmlTable + '</tr><tr class="table-warning">'

        thisQueryDate = datetime.date.today()

        htmlTable = htmlTable + "<td>" + str(dateWeekday(thisQueryDate)) + " (dags udlån / periode udlån / total)</td>"

        for location in models.Locations.objects.exclude(name='U/NORD').order_by('name'):

            criterionLaonDate = Q(loan_date=thisQueryDate)
            criterionLoanDateNot = ~Q(loan_date=thisQueryDate)
            criterionReturnDate = Q(return_date=thisQueryDate)
            criterionLocation = Q(location__name=location.name)
            criterionReturnNot = Q(returned=False)

            thisQuerysetLocationLoanDay = models.Loan_asset.objects.filter(criterionLaonDate & criterionReturnDate & criterionLocation & criterionReturnNot).count()
            thisQuerysetLocationLoanPeriod = models.Loan_asset.objects.filter(criterionLocation & criterionReturnNot & criterionLoanDateNot & criterionReturnDate).count()
            thisQuerysetLocationTotal = models.Loan_asset.objects.filter(criterionReturnDate & criterionLocation & criterionReturnNot).count()

            if thisQuerysetLocationLoanDay > 0 or thisQuerysetLocationLoanPeriod > 0 or thisQuerysetLocationTotal > 0:
                thisLink = '<a href="filter/' + location.name + '/' + str(thisQueryDate) + '/' + str(False) + '/currentDate/">'
                htmlTable = htmlTable + '<td><div style="text-align: center;">' + thisLink + str(thisQuerysetLocationLoanDay) + '/' + str(thisQuerysetLocationLoanPeriod) + '/' + str(thisQuerysetLocationTotal) + '</a></div></td>'
            else:
                htmlTable = htmlTable + '<td><div style="text-align: center;">' + str(
                    thisQuerysetLocationLoanDay) + '/' + str(thisQuerysetLocationLoanPeriod) + '/' + str(
                    thisQuerysetLocationTotal) + '</div></td>'

        iDate = 1


        htmlTable = htmlTable + "</tr>"


########Loan 30 days from now
        while iDate != 31:
            thisQueryDate = datetime.date.today() + datetime.timedelta(days=iDate)

            if "Lørdag" in str(dateWeekday(thisQueryDate)) or "Søndag" in str(dateWeekday(thisQueryDate)):
                htmlTable = htmlTable + '<tr class="table-secondary"><td>' + str(dateWeekday(thisQueryDate)) + '</td>'
            else:
                htmlTable = htmlTable + "<tr><td>" + str(dateWeekday(thisQueryDate)) + "</td>"

            for location in models.Locations.objects.exclude(name = 'U/NORD').order_by('name'):

                criterionReturnDate = Q(return_date=thisQueryDate)
                criterionLocation = Q(location__name=location.name)
                criterionReturnNot = Q(returned=False)

                thisQuerysetLocationTotal = models.Loan_asset.objects.filter(criterionReturnDate & criterionLocation & criterionReturnNot).count()



                if thisQuerysetLocationTotal > 0:
                    thisLink = '<a href="filter/' + location.name + '/' + str(thisQueryDate) + '/' + str(
                        False) + '/currentDate/">'
                    htmlTable = htmlTable + '<td><div style="text-align: center;">' + thisLink + str(thisQuerysetLocationTotal) + '</a></div></td>'
                else:
                    htmlTable = htmlTable + '<td></td>'

            htmlTable = htmlTable + "</tr>"
            iDate = iDate + 1

########Loan 30 days from now
        thisQueryDate
        htmlTable = htmlTable + "<tr class='table-success'><td>Udstyr der skal afleveres efter den " + thisQueryDate.strftime('%d/%m/%Y') + "</td>"
        for location in models.Locations.objects.exclude(name='U/NORD').order_by('name'):

            criterionReturnDate = Q(return_date__gt=thisQueryDate)
            criterionLocation = Q(location__name=location.name)
            criterionReturnNot = Q(returned=False)

            thisQuerysetLocationTotal = models.Loan_asset.objects.filter(
                criterionReturnDate & criterionLocation & criterionReturnNot).count()

            if thisQuerysetLocationTotal > 0:
                thisLink = '<a href="filter/' + location.name + '/' + str(thisQueryDate) + '/' + str(
                    False) + '/monthPlus/">'
                htmlTable = htmlTable + '<td><div style="text-align: center;">' + thisLink + str(
                    thisQuerysetLocationTotal) + '</a></div></td>'
            else:
                htmlTable = htmlTable + '<td></td>'


        context['loan_statTable'] = htmlTable + "</table>"
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
        asset_id = item.asset.id
        messages.success(request, 'Noteret udstyret som ikke afleveret')
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = True
        item.save()
        return redirect('asset_app_loan_asset_list')

    def returned_false(request, res_id):
        item = models.Loan_asset.objects.get(pk=res_id)
        item.returned = True
        asset_id = item.asset.id
        messages.success(request, 'Noteret udstyret som afleveret')
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = False
        item.save()
        return redirect('asset_app_loan_asset_list')

    def buttonSmsReturnLate(self, pk):
        smsButtonLateReturn(pk)
        return redirect('asset_app_loan_asset_detail', pk)

    def buttonSmsReturnReminder(self, pk):
        smsButtonReturnReminder(pk)
        return redirect('asset_app_loan_asset_detail', pk)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(returned=True).order_by('returned', 'return_date', 'loaner_name', 'asset')
        return queryset

@method_decorator(login_required, name='dispatch')
class Loan_assetListFilterView(generic.ListView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm
    template_name = "asset_app/loan_asset_filter_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context_entry = datetime.date.today()
        if self.kwargs['task'] == "late":
            if self.kwargs['loc_name'] == "any":
                context["loab_title"] = "Udlån oversigt over ikke afleveret til tiden"
            else:
                context["loab_title"] = "Udlån oversigt over ikke afleveret til tiden på {}".format(self.kwargs['loc_name'])
        elif self.kwargs['task'] == "currentDate":
            context["loab_title"] = "Forvented aflevering for {}, for følgende dato {}".format(self.kwargs['loc_name'], datetime.datetime.strptime(self.kwargs['return_date'], "%Y-%m-%d").strftime("%d/%m/%Y"))
        elif self.kwargs['task'] == "monthPlus":
            context["loab_title"] = "Forvented aflevering for {}, der skal afleveres efter den {}".format(self.kwargs['loc_name'], datetime.datetime.strptime(self.kwargs['return_date'], "%Y-%m-%d").strftime("%d/%m/%Y"))
        context["task"] = self.kwargs['loc_name']
        context["return_date"] = self.kwargs['return_date']
        context["returned"] = self.kwargs['returned']
        context["task"] = self.kwargs['task']
        context["today"] = new_context_entry
        return context

    def returned_true(self, loc_name, return_date, returned, task, pk):
        #task = self.kwargs.get("task")
        #return_date = self.kwargs.get("return_date")
        #loc_name = self.kwargs.get("loc_name")
        #returned = self.kwargs.get("returned")

        item = models.Loan_asset.objects.get(pk=pk)
        item.returned = False
        asset_id = item.asset.id
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = True
        item.save()
        return redirect('asset_app_loan_asset_list_filter', task=task, return_date=return_date, loc_name=loc_name, returned=returned)

    def returned_false(self, loc_name, return_date, returned, task, pk):

        item = models.Loan_asset.objects.get(pk=pk)
        item.returned = True
        asset_id = item.asset.id
        item.save()
        item = models.Asset.objects.get(pk=asset_id)
        item.is_loaned = False
        item.save()
        return redirect('asset_app_loan_asset_list_filter', task=task, return_date=return_date, loc_name=loc_name, returned=returned)

    def dropped_out(self, pk, dropped_out_status=False):
        item = models.Loan_asset.objects.get(pk=pk)
        item.dropped_out_of_school = dropped_out_status
        item.save()
        return redirect('asset_app_loan_asset_detail', pk=pk)

    def get_queryset(self):

        task = self.kwargs.get("task")
        return_date = self.kwargs.get("return_date")
        loc_name = self.kwargs.get("loc_name")
        returned = self.kwargs.get("returned")

        if task == "late":
            criterionReturnDate = Q(return_date__lt=return_date)
        elif task == "currentDate":
            criterionReturnDate = Q(return_date=return_date)
        elif task == "monthPlus":
            criterionReturnDate = Q(return_date__gte=return_date)
        criterionLocation = Q(location__name=loc_name)
        criterionReturnState = Q(returned=returned)
        if loc_name == "any" and task == "drop_out":
            queryset = super().get_queryset().filter(dropped_out_of_school=True).exclude(returned=True).order_by('-dropped_out_of_school', 'return_date', 'loaner_name', 'asset')
        elif loc_name == "any" and task == "all":
            queryset = super().get_queryset().exclude(returned=True).exclude(asset=None).order_by('-dropped_out_of_school', 'return_date', 'loaner_name', 'asset')
        elif loc_name == "any":
            queryset = super().get_queryset().filter(criterionReturnState & criterionReturnDate).order_by('-dropped_out_of_school', 'return_date', 'loaner_name', 'asset')
        else:
            queryset = super().get_queryset().filter(criterionLocation & criterionReturnState & criterionReturnDate).order_by('-dropped_out_of_school', 'return_date', 'loaner_name', 'asset')

        return queryset

@method_decorator(login_required, name='dispatch')
class Loan_assetListExcelView(generic.DetailView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm


    def get(self, request):
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Personlig uglån")

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatDate = workbook.add_format({'num_format': 'dd/mm/yy'})

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})

        formatGreen = workbook.add_format({'bg_color': '#5A916E',
                                         'font_color': '#FFFFFF'})

        thisColumn = 1
        thisRow = 2


        worksheet_s.write(thisRow, 1, ugettext("Udlåner"), header)
        worksheet_s.write(thisRow, 2, ugettext("Udd navn"), header)
        worksheet_s.write(thisRow, 3, ugettext("Udd slutdato"), header)
        worksheet_s.write(thisRow, 4, ugettext("Udlånt fra"), header)
        worksheet_s.write(thisRow, 5, ugettext("Ansat/Elev"), header)
        worksheet_s.write(thisRow, 6, ugettext("Telefon nummer"), header)
        worksheet_s.write(thisRow, 7, ugettext("Email"), header)
        worksheet_s.write(thisRow, 8, ugettext("Udstyrs navn"), header)
        worksheet_s.write(thisRow, 9, ugettext("Udstyrs type"), header)
        worksheet_s.write(thisRow, 10, ugettext("Udstyr mærke"), header)
        worksheet_s.write(thisRow, 11, ugettext("Serienummer"), header)
        worksheet_s.write(thisRow, 12, ugettext("Udlånt fra"), header)
        worksheet_s.write(thisRow, 13, ugettext("Udlånt til"), header)
        worksheet_s.write(thisRow, 14, ugettext("Retuneret"), header)



        thisRow = thisRow +1
        queryset = models.Loan_asset.objects.filter(returned = False).order_by('returned', 'loaner_name', 'asset')

        for idx, data in enumerate(queryset):
            row = thisRow + idx

            if data.return_date >= datetime.date.today() and data.returned == False:
                if data.asset:
                    worksheet_s.write_number(row, 0, idx + 1)
                    worksheet_s.write_string(row, 1, data.loaner_name)
                    if data.eduName is not None:
                        worksheet_s.write_string(row, 2, data.eduName)
                    if data.endEduDate is not None:
                        worksheet_s.write_string(row, 3, datetime.datetime.strptime(str(data.endEduDate), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    worksheet_s.write_string(row, 4, data.location.name)
                    worksheet_s.write_string(row, 5, data.loaner_type.name)
                    worksheet_s.write_string(row, 6, data.loaner_telephone_number)
                    worksheet_s.write_string(row, 7, data.loaner_email)
                    if data.asset.name is not None:
                        worksheet_s.write_string(row, 8, data.asset.name)
                        worksheet_s.write_string(row, 9, data.asset.model_hardware.asset_type.name)
                        worksheet_s.write_string(row, 10, data.asset.model_hardware.brand.name+' '+ data.asset.model_hardware.name)
                        worksheet_s.write_string(row, 11, data.asset.serial)
                    worksheet_s.write_string(row, 12, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    worksheet_s.write_string(row, 13, datetime.datetime.strptime(str(data.return_date), '%Y-%m-%d').strftime('%d/%m/%Y'))
                    if data.returned == True:
                        returnedValue = "Ja"
                    else:
                        returnedValue = "Nej"
                    worksheet_s.write_string(row, 14, returnedValue)

            elif data.return_date < datetime.date.today() and data.returned == False:
                if data.asset:
                    worksheet_s.write_number(row, 0, idx + 1, formatRed)
                    worksheet_s.write_string(row, 1, data.loaner_name, formatRed)
                    if data.eduName is not None:
                        worksheet_s.write_string(row, 2, data.eduName, formatRed)
                    else:
                        worksheet_s.write_string(row, 2, " ", formatRed)
                    if data.endEduDate is not None:
                        worksheet_s.write_string(row, 3, datetime.datetime.strptime(str(data.endEduDate), '%Y-%m-%d').strftime('%d/%m/%Y'), formatRed)
                    else:
                        worksheet_s.write_string(row, 3, " ", formatRed)
                    worksheet_s.write_string(row, 4, data.location.name, formatRed)
                    worksheet_s.write_string(row, 5, data.loaner_type.name, formatRed)
                    worksheet_s.write_string(row, 6, data.loaner_telephone_number, formatRed)
                    worksheet_s.write_string(row, 7, data.loaner_email, formatRed)
                    if data.asset.name is not None:
                        worksheet_s.write_string(row, 8, data.asset.name, formatRed)
                        worksheet_s.write_string(row, 9, data.asset.model_hardware.asset_type.name, formatRed)
                        worksheet_s.write_string(row, 10, data.asset.model_hardware.brand.name+' '+ data.asset.model_hardware.name, formatRed)
                    else:
                        worksheet_s.write_string(row, 8, " ", formatRed)
                        worksheet_s.write_string(row, 9, " ", formatRed)
                        worksheet_s.write_string(row, 10, " ", formatRed)
                    worksheet_s.write_string(row, 11, data.asset.serial, formatRed)
                    worksheet_s.write_string(row, 12, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatRed)
                    worksheet_s.write_string(row, 13, datetime.datetime.strptime(str(data.return_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatRed)
                    if data.returned == True:
                        returnedValue = "Ja"
                    else:
                        returnedValue = "Nej"
                    worksheet_s.write_string(row, 14, returnedValue, formatRed)

            else:
                if data.asset:
                    worksheet_s.write_number(row, 0, idx + 1, formatGreen)
                    worksheet_s.write_string(row, 1, data.loaner_name, formatGreen)
                    if data.eduName is not None:
                        worksheet_s.write_string(row, 2, data.eduName, formatGreen)
                    else:
                        worksheet_s.write_string(row, 2, " ", formatGreen)
                    if data.endEduDate is not None:
                        worksheet_s.write_string(row, 3, datetime.datetime.strptime(str(data.endEduDate), '%Y-%m-%d').strftime('%d/%m/%Y'), formatGreen)
                    else:
                        worksheet_s.write_string(row, 3, " ", formatGreen)
                    worksheet_s.write_string(row, 4, data.location.name, formatGreen)
                    worksheet_s.write_string(row, 5, data.loaner_type.name, formatGreen)
                    worksheet_s.write_string(row, 6, data.loaner_telephone_number, formatGreen)
                    worksheet_s.write_string(row, 7, data.loaner_email, formatGreen)
                    if data.asset.name is not None:
                        worksheet_s.write_string(row, 8, data.asset.name, formatGreen)
                        worksheet_s.write_string(row, 9, data.asset.model_hardware.asset_type.name, formatGreen)
                        worksheet_s.write_string(row, 10, data.asset.model_hardware.brand.name+' '+ data.asset.model_hardware.name, formatGreen)
                    else:
                        worksheet_s.write_string(row, 8, " ", formatGreen)
                        worksheet_s.write_string(row, 9, " ", formatGreen)
                        worksheet_s.write_string(row, 10, " ", formatGreen)
                    worksheet_s.write_string(row, 11, data.asset.serial, formatGreen)
                    worksheet_s.write_string(row, 12, datetime.datetime.strptime(str(data.loan_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatGreen)
                    worksheet_s.write_string(row, 13, datetime.datetime.strptime(str(data.return_date), '%Y-%m-%d').strftime('%d/%m/%Y'), formatGreen)
                    if data.returned == True:
                        returnedValue = "Ja"
                    else:
                        returnedValue = "Nej"
                    worksheet_s.write_string(row, 14, returnedValue, formatGreen)

            if not data.asset:
                thisRow = thisRow - 1

            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 15)
        worksheet_s.set_column('E:E', 15)
        worksheet_s.set_column('F:F', 30)
        worksheet_s.set_column('G:G', 30)
        worksheet_s.set_column('H:H', 20)
        worksheet_s.set_column('H:H', 30)
        worksheet_s.set_column('I:I', 35)
        worksheet_s.set_column('J:J', 15)
        worksheet_s.set_column('K:K', 15)
        worksheet_s.set_column('L:L', 15)
        worksheet_s.set_column('M:M', 15)


        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = 'Personligt_udlån_' + str(datetime.date.today()) + '.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


@method_decorator(login_required, name='dispatch')
class Loan_assetCreateView(generic.CreateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

    def get_queryset(self):


        queryset = super().get_queryset().order_by('asset__model_hardware__asset_type', 'asset.name')
        return queryset
    @receiver(post_save, sender=models.Loan_asset)
    def create_transaction(sender, instance, created, **kwargs):
        if created:
            asset = instance.asset
            asset.is_loaned = True

            asset.save(update_fields=["is_loaned"])  # updates only `is_loaned

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user_email = str(self.kwargs.get("user_email"))

        context['loans'] = models.Loan_asset.objects.filter(loaner_email=str(user_email)).exclude(returned=True)
        context['user_email'] = user_email
        return context



@method_decorator(login_required, name='dispatch')
class Loan_assetDetailView(generic.DetailView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['smsLogs'] = models.SmsLog.objects.filter(loan_asset_id=self.kwargs.get('pk')).order_by('-sms_timestamp')
        return context


@method_decorator(login_required, name='dispatch')
class Loan_assetUpdateView(generic.UpdateView):
    model = models.Loan_asset
    form_class = forms.Loan_assetUpdateForm
    pk_url_kwarg = "pk"

class Loan_assetViewAPI(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = models.Loan_asset.objects.all()
    serializer_class = Loan_assetSerializer

    expired_param = openapi.Parameter(
        'expired', openapi.IN_QUERY,
        description="Set to 'true' to filter loans where the return_date has passed and returned is False and only searches for students",
        type=openapi.TYPE_BOOLEAN
    )

    @swagger_auto_schema(manual_parameters=[expired_param])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.Loan_asset.objects.all()

        # Custom filter for expired loans that are not returned
        expired = self.request.query_params.get('expired', None)
        if expired is not None and expired.lower() == 'true':
            queryset = queryset.filter(return_date__lt=datetime.datetime.now(), returned=False, loaner_type__name='Elev')

        return queryset


#@method_decorator(login_required, name='dispatch') So that HEFA can view it
class Loan_assetListViewStudentDeliquent(generic.ListView):
    model = models.Loan_asset
    form_class = forms.Loan_assetForm
    template_name = 'asset_app/loan_asset_list_student_deliquent.html'

    def get_queryset(self):
        today = date.today()  # Get today's date
        queryset = super().get_queryset()
        # Filter based on return_date and loaner_type
        queryset = queryset.filter(
            Q(returned=False) &
            Q(return_date__lt=today)
        ).exclude(loaner_type__name="Ansat").order_by('dropped_out_of_school', 'responsible_teacher_initials', 'eduName')
        return queryset

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
        queryset = super().get_queryset().filter(room__location__name=location).filter(may_be_loaned=True).order_by('name')
        return queryset





@method_decorator(login_required, name='dispatch')
class LocationLaptopListExcelView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm

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

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})

        worksheet_s.write(2, 1, ugettext("Navn"), header)
        worksheet_s.write(2, 2, ugettext("Afdeling"), header)
        worksheet_s.write(2, 3, ugettext("Placering"), header)
        worksheet_s.write(2, 4, ugettext("Lokale type"), header)
        worksheet_s.write(2, 5, ugettext("Mærke og model"), header)
        worksheet_s.write(2, 6, ugettext("Udstyr type"), header)
        worksheet_s.write(2, 7, ugettext("Serienummer"), header)
        worksheet_s.write(2, 8, ugettext("Må udlånes"), header)
        worksheet_s.write(2, 9, ugettext("Meldt savnede"), header)

        if location=="all":
            queryset = super().get_queryset().order_by('name')
        else:
            queryset = super().get_queryset().filter(room__location__name=location).filter(model_hardware__asset_type__name="Bærebar").order_by('name')

        for idx, data in enumerate(queryset):
            row = 3 + idx

            if data.missing:
                worksheet_s.write_number(row, 0, idx + 1, formatRed)
                worksheet_s.write_string(row, 1, data.name, formatRed)
                worksheet_s.write_string(row, 2, data.room.location.name, formatRed)
                worksheet_s.write_string(row, 3, data.room.name, formatRed)
                worksheet_s.write_string(row, 4, data.room.room_type.name, formatRed)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name + ' ' + data.model_hardware.name, formatRed)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name, formatRed)
                worksheet_s.write_string(row, 7, data.serial, formatRed)
                worksheet_s.write_boolean(row, 8, data.may_be_loaned, formatRed)
                worksheet_s.write_boolean(row, 9, data.missing, formatRed)
            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.name)
                worksheet_s.write_string(row, 2, data.room.location.name)
                worksheet_s.write_string(row, 3, data.room.name)
                worksheet_s.write_string(row, 4, data.room.room_type.name)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name + ' ' + data.model_hardware.name)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name)
                worksheet_s.write_string(row, 7, data.serial)
                worksheet_s.write_boolean(row, 8, data.may_be_loaned)
                worksheet_s.write_boolean(row, 9, data.missing)


            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 30)
        worksheet_s.set_column('E:E', 35)
        worksheet_s.set_column('F:F', 45)
        worksheet_s.set_column('G:G', 15)
        worksheet_s.set_column('H:H', 30)
        worksheet_s.set_column('I:I', 15)
        worksheet_s.set_column('J:J', 20)


        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        if location == "all":
            filename = 'Udstyr-´'+str(datetime.date.today())+'.xlsx'
        else:
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
class Model_hardwareDetailExcelView(generic.ListView):
    model = models.Asset
    form_class = forms.AssetForm

    def get(self, request, pk):

        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet("Udstyr")

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})

        worksheet_s.write(2, 1, ugettext("Udstyrs navn"), header)
        worksheet_s.write(2, 2, ugettext("Serienummer"), header)
        worksheet_s.write(2, 3, ugettext("Placering"), header)
        worksheet_s.write(2, 4, ugettext("Model"), header)
        worksheet_s.write(2, 5, ugettext("Mærke"), header)
        worksheet_s.write(2, 6, ugettext("Udstyr type"), header)
        worksheet_s.write(2, 7, ugettext("Må udlånes"), header)
        worksheet_s.write(2, 8, ugettext("Meldt savnede"), header)

        queryset = models.Asset.objects.filter(model_hardware_id=pk).order_by('name')

        for idx, data in enumerate(queryset):
            row = 3 + idx

            if data.missing:

                worksheet_s.write_number(row, 0, idx + 1, formatRed)
                worksheet_s.write_string(row, 1, data.name, formatRed)
                worksheet_s.write_string(row, 2, data.serial, formatRed)
                worksheet_s.write_string(row, 3, data.room.name+" :: "+ data.room.location.name +" :: "+data.room.room_type.name, formatRed)
                worksheet_s.write_string(row, 4, data.model_hardware.name, formatRed)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name, formatRed)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name, formatRed)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned, formatRed)
                worksheet_s.write_boolean(row, 8, data.missing, formatRed)
            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.name)
                worksheet_s.write_string(row, 2, data.serial)
                worksheet_s.write_string(row, 3,
                                         data.room.name + " :: " + data.room.location.name + " :: " + data.room.room_type.name)
                worksheet_s.write_string(row, 4, data.model_hardware.name)
                worksheet_s.write_string(row, 5, data.model_hardware.brand.name)
                worksheet_s.write_string(row, 6, data.model_hardware.asset_type.name)
                worksheet_s.write_boolean(row, 7, data.may_be_loaned)
                worksheet_s.write_boolean(row, 8, data.missing)

            # the rest of the data

        worksheet_s.set_column('B:B', 30)
        worksheet_s.set_column('C:C', 15)
        worksheet_s.set_column('D:D', 40)
        worksheet_s.set_column('E:E', 25)
        worksheet_s.set_column('F:F', 30)
        worksheet_s.set_column('G:G', 35)
        worksheet_s.set_column('H:H', 15)
        worksheet_s.set_column('I:I', 15)
        worksheet_s.set_column('J:J', 15)


        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.

        filename = 'Udstyr-'+str(datetime.date.today())+'.xlsx'

        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response


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

    def delete(request, pk):
        item = models.Room.objects.get(pk=pk)
        item.delete()
        messages.success(request, 'Rum er nu blevet slettet')
        return redirect('asset_app_room_list')

    def inspectToday(request, pk):
        item = models.Room.objects.get(pk=pk)
        item.last_inspected = datetime.date.today()
        item.save()
        messages.success(request, 'Rum "'+item.name+'" er nu blevet registret som gennemgået idag')
        return redirect('asset_app_room_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context_entry_today = datetime.date.today()
        context_entry_overdue = datetime.date.today() - datetime.timedelta(days=90)
        context_entry_inspection_time = datetime.date.today() - datetime.timedelta(days=76)
        context['rooms'] = models.Room.objects.exclude(room_type__name='Skole').exclude(
            room_type__name='Afdeling').exclude(last_inspected=None).exclude(last_inspected__gt=context_entry_inspection_time).order_by('last_inspected', 'location', 'name')
        context["today"] = context_entry_today
        context["overdue"] = context_entry_overdue
        context["inspection_time"] = context_entry_inspection_time
        return context


@method_decorator(login_required, name='dispatch')
class RoomCreateView(generic.CreateView):
    model = models.Room
    form_class = forms.RoomForm


@method_decorator(login_required, name='dispatch')
class RoomDetailView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm

    def may_be_loaned_true(request, asset, pk):
        item = models.Asset.objects.get(pk=asset)
        item.may_be_loaned = True
        messages.success(request, 'Udstyret må nu udlånes')
        item.save()
        return redirect('asset_app_room_detail', pk=pk)

    def may_be_loaned_false(request, asset, pk):
        item = models.Asset.objects.get(pk=asset)
        item.may_be_loaned = False
        messages.success(request, 'Udstyret må ikke udlånes')
        item.save()
        return redirect('asset_app_room_detail', pk=pk)

@method_decorator(login_required, name='dispatch')
class RoomPDFDetailView(PDFTemplateResponseMixin, generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm
    template_name = 'asset_app/room_detail_to-pdf.html'

@method_decorator(login_required, name='dispatch')
class RoomDetailExcelView(generic.DetailView):
    model = models.Room
    form_class = forms.RoomForm


    def get(self, request, pk):

        queryset = super().get_queryset().filter(id=pk).order_by('name')
        for object in queryset:
            name = object.name
            location = object.location.name
            room_type = object.room_type.name
            image_date = object.image_date
            image = object.image
            last_inspected = object.last_inspected



        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Here we will adding the code to add data
        worksheet_s = workbook.add_worksheet(name+"-"+location)

        header = workbook.add_format({
            'bg_color': '#F7F7F7',
            'color': 'black',
            'align': 'center',
            'valign': 'top',
            'border': 1
        })

        formatDate = workbook.add_format({'num_format': 'dd/mm/yy'})

        formatRed = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})
        thisColumn = 1
        thisRow = 1

        worksheet_s.write(2, thisColumn, ugettext("Rum:"), header)
        worksheet_s.write(3, thisColumn, ugettext("Afdeling:"), header)
        worksheet_s.write(4, thisColumn, ugettext("Rum type:"), header)
        worksheet_s.write(5, thisColumn, ugettext("Lokale sidst gennemgået:"), header)
        if image:
            worksheet_s.write(6, thisColumn, ugettext("Billede dato:"), header)


        thisColumn = 2

        worksheet_s.write_string(2, thisColumn, name)
        worksheet_s.write_string(3, thisColumn, location)
        worksheet_s.write_string(4, thisColumn, room_type)
        if image:
            #worksheet_s.insert_image(5, thisColumn, image)
            url = 'https://unord-tools-django-project-static.s3.eu-central-1.amazonaws.com/media/public/'+str(image)
            image_data = BytesIO(urlopen(url).read())
            worksheet_s.insert_image('D2', name, {'image_data': image_data, 'x_scale': 0.1, 'y_scale': 0.1})
            worksheet_s.write_string(6, thisColumn, datetime.datetime.strptime(str(image_date), '%Y-%m-%d').strftime('%m/%d/%Y'))

        worksheet_s.write_string(5, thisColumn, datetime.datetime.strptime(str(last_inspected), '%Y-%m-%d').strftime('%m/%d/%Y'))

        if image:
            thisRow = 23
        else:
            thisRow = 13

        worksheet_s.write(thisRow, 1, ugettext("Navn"), header)
        worksheet_s.write(thisRow, 2, ugettext("Mærke og model"), header)
        worksheet_s.write(thisRow, 3, ugettext("Udstyr type"), header)
        worksheet_s.write(thisRow, 4, ugettext("Serienummer"), header)
        worksheet_s.write(thisRow, 5, ugettext("Må udlånes"), header)
        worksheet_s.write(thisRow, 6, ugettext("Meldt savnede"), header)


        thisRow = thisRow +1
        queryset = models.Asset.objects.filter(room = pk).order_by('name')

        for idx, data in enumerate(queryset):
            row = thisRow + idx

            if data.missing:
                worksheet_s.write_number(row, 0, idx + 1, formatRed)
                worksheet_s.write_string(row, 1, data.name, formatRed)
                worksheet_s.write_string(row, 2, data.model_hardware.brand.name + ' ' + data.model_hardware.name, formatRed)
                worksheet_s.write_string(row, 3, data.model_hardware.asset_type.name, formatRed)
                worksheet_s.write_string(row, 4, data.serial, formatRed)
                worksheet_s.write_boolean(row, 5, data.may_be_loaned, formatRed)
                worksheet_s.write_boolean(row, 6, data.missing, formatRed)
            else:
                worksheet_s.write_number(row, 0, idx + 1)
                worksheet_s.write_string(row, 1, data.name)
                worksheet_s.write_string(row, 2, data.model_hardware.brand.name + ' ' + data.model_hardware.name)
                worksheet_s.write_string(row, 3, data.model_hardware.asset_type.name)
                worksheet_s.write_string(row, 4, data.serial)
                worksheet_s.write_boolean(row, 5, data.may_be_loaned)
                worksheet_s.write_boolean(row, 6, data.missing)


            # the rest of the data

        worksheet_s.set_column('B:B', 40)
        worksheet_s.set_column('C:C', 40)
        worksheet_s.set_column('D:D', 40)
        worksheet_s.set_column('E:E', 35)
        worksheet_s.set_column('F:F', 15)
        worksheet_s.set_column('G:G', 15)


        workbook.close()
        xlsx_data = output.getvalue()

        # Rewind the buffer.
        output.seek(0)

        # Set up the Http response.
        filename = name + '-' + location + '-' + str(datetime.date.today()) + '.xlsx'
        response = HttpResponse(
            output,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename

        return response



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


@method_decorator(login_required, name='dispatch')
class SmsListView(generic.ListView):
    model = models.Sms
    form_class = forms.SmsForm

    def delete(request, del_id):
        item = models.Sms.objects.get(pk=del_id)
        item.delete()
        messages.success(request, 'Sms type er nu slettet')
        return redirect('asset_app_sms_list')


@method_decorator(login_required, name='dispatch')
class SmsCreateView(generic.CreateView):
    model = models.Sms
    form_class = forms.SmsForm


@method_decorator(login_required, name='dispatch')
class SmsDetailView(generic.DetailView):
    model = models.Sms
    form_class = forms.SmsForm


@method_decorator(login_required, name='dispatch')
class SmsUpdateView(generic.UpdateView):
    model = models.Sms
    form_class = forms.SmsForm
    pk_url_kwarg = "pk"

@method_decorator(login_required, name='dispatch')
class SmsLogListView(generic.ListView):
    model = models.SmsLog
    form_class = forms.SmsLogForm

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-sms_timestamp')
        return queryset



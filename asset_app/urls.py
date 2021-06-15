from django.urls import path, include
from rest_framework import routers
from django.conf.urls.static import settings, static
from . import api
from . import views


router = routers.DefaultRouter()
router.register("asset", api.AssetViewSet)
router.register("asset_type", api.Asset_typeViewSet)
router.register("brand", api.BrandViewSet)
router.register("bundle_reservation", api.Bundle_reservationViewSet)
router.register("loan_asset", api.Loan_assetViewSet)
router.register("loaner_type", api.Loaner_typeViewSet)
router.register("locations", api.LocationsViewSet)
router.register("loaner_type", api.Loaner_typeViewSet)
router.register("model_hardware", api.Model_hardwareViewSet)
router.register("one_2_one_info", api.One2OneInfoViewSet)
router.register("one_2_one_info_log", api.One2OneInfoLogViewSet)
router.register("room", api.RoomViewSet)
router.register("room_type", api.Room_typeViewSet)
router.register("Routines", api.RoutinesViewSet)
router.register("RoutineLog", api.RoutineLogViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("asset_app/asset/", views.AssetListView.as_view(), name="asset_app_asset_list"),
    path("asset_app/asset/create/", views.AssetCreateView.as_view(), name="asset_app_asset_create"),
    path("asset_app/asset/detail/<int:pk>/", views.AssetDetailView.as_view(), name="asset_app_asset_detail"),
    path("asset_app/asset/update/<int:pk>/", views.AssetUpdateView.as_view(), name="asset_app_asset_update"),
    path("asset_app/asset/delete/<int:pk>/", views.AssetListView.delete, name="asset_app_asset_delete"),
    path("asset_app/asset_type/", views.Asset_typeListView.as_view(), name="asset_app_asset_type_list"),
    path("asset_app/asset_type/create/", views.Asset_typeCreateView.as_view(), name="asset_app_asset_type_create"),
    path("asset_app/asset_type/detail/<int:pk>/", views.Asset_typeDetailView.as_view(), name="asset_app_asset_type_detail"),
    path("asset_app/asset_type/update/<int:pk>/", views.Asset_typeUpdateView.as_view(), name="asset_app_asset_type_update"),
    path("asset_app/asset_type/delete/<int:pk>/", views.Asset_typeListView.delete, name="asset_app_asset_type_delete"),
    path("asset_app/brand/", views.BrandListView.as_view(), name="asset_app_brand_list"),
    path("asset_app/brand/create/", views.BrandCreateView.as_view(), name="asset_app_brand_create"),
    path("asset_app/brand/detail/<int:pk>/", views.BrandDetailView.as_view(), name="asset_app_brand_detail"),
    path("asset_app/brand/update/<int:pk>/", views.BrandUpdateView.as_view(), name="asset_app_brand_update"),
    path("asset_app/brand/delete/<int:pk>/", views.BrandListView.delete, name="asset_app_brand_delete"),
    path("asset_app/bundle_reservation/", views.Bundle_reservationListView.as_view(), name="asset_app_bundle_reservation_list"),
    path("asset_app/bundle_reservation/create/", views.Bundle_reservationCreateView.as_view(), name="asset_app_bundle_reservation_create"),
    path("asset_app/bundle_reservation/detail/<int:pk>/", views.Bundle_reservationDetailView.as_view(), name="asset_app_bundle_reservation_detail"),
    path("asset_app/bundle_reservation/update/<int:pk>/", views.Bundle_reservationUpdateView.as_view(), name="asset_app_bundle_reservation_update"),
    path('asset_app/bundle_reservation/returned_true/<res_id>', views.Bundle_reservationListView.returned_true, name='asset_app_bundle_reservation_returned_true'),
    path('asset_app/bundle_reservation/returned_false/<res_id>', views.Bundle_reservationListView.returned_false, name='asset_app_bundle_reservation_returned_false'),
    path("asset_app/dashboard/", views.Dashboard.as_view(), name="asset_app_dashboard"),
    path("asset_app/loan_asset/", views.Loan_assetListView.as_view(), name="asset_app_loan_asset_list"),
    path("asset_app/loan_asset/create/", views.Loan_assetCreateView.as_view(), name="asset_app_loan_asset_create"),
    path("asset_app/loan_asset/detail/<int:pk>/", views.Loan_assetDetailView.as_view(), name="asset_app_loan_asset_detail"),
    path("asset_app/loan_asset/update/<int:pk>/", views.Loan_assetUpdateView.as_view(), name="asset_app_loan_asset_update"),
    path('asset_app/loan_asset/returned_true/<res_id>', views.Loan_assetListView.returned_true, name='asset_app_loan_asset_returned_true'),
    path('asset_app/loan_asset/returned_false/<res_id>', views.Loan_assetListView.returned_false, name='asset_app_loan_asset_returned_false'),
    path("asset_app/loaner_type/", views.Loaner_typeListView.as_view(), name="asset_app_loaner_type_list"),
    path("asset_app/loaner_type/create/", views.Loaner_typeCreateView.as_view(), name="asset_app_loaner_type_create"),
    path("asset_app/loaner_type/detail/<int:pk>/", views.Loaner_typeDetailView.as_view(), name="asset_app_loaner_type_detail"),
    path("asset_app/loaner_type/update/<int:pk>/", views.Loaner_typeUpdateView.as_view(), name="asset_app_loaner_type_update"),
    path("asset_app/loaner_type/delete/<int:pk>/", views.Loaner_typeListView.delete, name="asset_app_loaner_type_delete"),
    path("asset_app/locations/", views.LocationsListView.as_view(), name="asset_app_locations_list"),
    path("asset_app/locations/create/", views.LocationsCreateView.as_view(), name="asset_app_locations_create"),
    path("asset_app/locations/detail/<int:pk>/", views.LocationsDetailView.as_view(), name="asset_app_locations_detail"),
    path("asset_app/locations/update/<int:pk>/", views.LocationsUpdateView.as_view(), name="asset_app_locations_update"),
    path("asset_app/locations/delete/<int:pk>/", views.LocationsListView.delete, name="asset_app_locations_delete"),
    path("asset_app/model_hardware/", views.Model_hardwareListView.as_view(), name="asset_app_model_hardware_list"),
    path("asset_app/model_hardware/create/", views.Model_hardwareCreateView.as_view(), name="asset_app_model_hardware_create"),
    path("asset_app/model_hardware/detail/<int:pk>/", views.Model_hardwareDetailView.as_view(), name="asset_app_model_hardware_detail"),
    path("asset_app/model_hardware/update/<int:pk>/", views.Model_hardwareUpdateView.as_view(), name="asset_app_model_hardware_update"),
    path("asset_app/model_hardware/delete/<int:pk>/", views.Model_hardwareListView.delete, name="asset_app_model_hardware_delete"),
    path("asset_app/one2one/", views.One2OneInfoListView.as_view(), name="asset_app_one2one_list"),
    path("asset_app/one2one/completed_true/<one_two_one_id>", views.One2OneInfoListView.completed_true, name="asset_app_one2one_completed_true"),
    path("asset_app/one2one/completed_false/<one_two_one_id>", views.One2OneInfoListView.completed_false, name="asset_app_one2one_completed_false"),
    path("asset_app/one2one/create/", views.One2OneInfoCreateView.as_view(), name="asset_app_one2one_create"),
    path("asset_app/one2one/detail/<int:pk>/", views.One2OneInfoDetailView.as_view(), name="asset_app_one2one_detail"),
    path("asset_app/one2one/update/<int:pk>/", views.One2OneInfoUpdateView.as_view(), name="asset_app_one2one_update"),
    path("asset_app/one2one/delete/<int:pk>/", views.One2OneInfoListView.delete, name="asset_app_one2one_delete"),
    path("asset_app/one2one_log/", views.One2OneInfoLogListView.as_view(), name="asset_app_one2one_log_list"),
    path("asset_app/one2one_log/create/", views.One2OneInfoLogCreateView.as_view(), name="asset_app_one2one_log_create"),
    path("asset_app/one2one_log/detail/<int:pk>/", views.One2OneInfoLogDetailView.as_view(), name="asset_app_one2one_log_detail"),
    path("asset_app/one2one_log/update/<int:pk>/", views.One2OneInfoLogUpdateView.as_view(), name="asset_app_one2one_log_update"),
    path("asset_app/one2one_log/delete/<int:pk>/", views.One2OneInfoLogListView.delete, name="asset_app_one2one_log_delete"),
    path("asset_app/room/", views.RoomListView.as_view(), name="asset_app_room_list"),
    path("asset_app/room/create/", views.RoomCreateView.as_view(), name="asset_app_room_create"),
    path("asset_app/room/detail/<int:pk>/", views.RoomDetailView.as_view(), name="asset_app_room_detail"),
    path("asset_app/room/detail_pdf/", views.RoomPDFDetailView.export_pdf_save, name="asset_app_room_detail_to_pdf_save"),
    path("asset_app/room/detail_pdf/<int:pk>/", views.RoomPDFDetailView, name="asset_app_room_detail_to_pdf_view"),
    path("asset_app/room/update/<int:pk>/", views.RoomUpdateView.as_view(), name="asset_app_room_update"),
    path("asset_app/room/delete/<int:pk>/", views.RoomListView.delete, name="asset_app_room_delete"),
    path("asset_app/room_type/", views.Room_typeListView.as_view(), name="asset_app_room_type_list"),
    path("asset_app/room_type/create/", views.Room_typeCreateView.as_view(), name="asset_app_room_type_create"),
    path("asset_app/room_type/detail/<int:pk>/", views.Room_typeDetailView.as_view(), name="asset_app_room_type_detail"),
    path("asset_app/room_type/update/<int:pk>/", views.Room_typeUpdateView.as_view(), name="asset_app_room_type_update"),
    path("asset_app/room_type/delete/<int:pk>/", views.Room_typeListView.delete, name="asset_app_room_type_delete"),
    path("asset_app/Routines/", views.RoutinesListView.as_view(), name="asset_app_routines_list"),
    path("asset_app/Routines/create/", views.RoutinesCreateView.as_view(), name="asset_app_routines_create"),
    path("asset_app/Routines/detail/<int:pk>/", views.RoutinesDetailView.as_view(), name="asset_app_routines_detail"),
    path("asset_app/Routines/update/<int:pk>/", views.RoutinesUpdateView.as_view(), name="asset_app_routines_update"),
    path("asset_app/RoutineLog/", views.RoutineLogListView.as_view(), name="asset_app_routineLog_list"),
    path("asset_app/RoutineLog/create/", views.RoutineLogCreateView.as_view(), name="asset_app_routineLog_create"),
    path("asset_app/RoutineLog/detail/<int:pk>/", views.RoutineLogDetailView.as_view(), name="asset_app_routineLog_detail"),
    path("asset_app/RoutineLog/update/<int:pk>/", views.RoutineLogUpdateView.as_view(), name="asset_app_routineLog_update"),
    path("search/", views.SearchView.as_view(), name="asset_app_search"),



]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
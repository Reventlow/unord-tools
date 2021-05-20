from django.urls import path, include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from . import api
from . import views


router = routers.DefaultRouter()
router.register("locations", api.LocationsViewSet)
router.register("asset_type", api.Asset_typeViewSet)
router.register("loan_asset", api.Loan_assetViewSet)
router.register("room", api.RoomViewSet)
router.register("asset", api.AssetViewSet)
router.register("loaner_type", api.Loaner_typeViewSet)
router.register("model", api.ModelViewSet)

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("asset_app/asset/", views.AssetListView.as_view(), name="asset_app_asset_list"),
    path("asset_app/asset/create/", views.AssetCreateView.as_view(), name="asset_app_asset_create"),
    path("asset_app/asset/detail/<int:pk>/", views.AssetDetailView.as_view(), name="asset_app_asset_detail"),
    path("asset_app/asset/update/<int:pk>/", views.AssetUpdateView.as_view(), name="asset_app_asset_update"),
    path("asset_app/asset_type/", views.Asset_typeListView.as_view(), name="asset_app_asset_type_list"),
    path("asset_app/asset_type/create/", views.Asset_typeCreateView.as_view(), name="asset_app_asset_type_create"),
    path("asset_app/asset_type/detail/<int:pk>/", views.Asset_typeDetailView.as_view(), name="asset_app_asset_type_detail"),
    path("asset_app/asset_type/update/<int:pk>/", views.Asset_typeUpdateView.as_view(), name="asset_app_asset_type_update"),
    path("asset_app/brand/", views.BrandListView.as_view(), name="asset_app_brand_list"),
    path("asset_app/brand/create/", views.BrandCreateView.as_view(), name="asset_app_brand_create"),
    path("asset_app/brand/detail/<int:pk>/", views.BrandDetailView.as_view(), name="asset_app_brand_detail"),
    path("asset_app/brand/update/<int:pk>/", views.BrandUpdateView.as_view(), name="asset_app_brand_update"),
    path("asset_app/loan_asset/", views.Loan_assetListView.as_view(), name="asset_app_loan_asset_list"),
    path("asset_app/loan_asset/create/", views.Loan_assetCreateView.as_view(), name="asset_app_loan_asset_create"),
    path("asset_app/loan_asset/detail/<int:pk>/", views.Loan_assetDetailView.as_view(), name="asset_app_loan_asset_detail"),
    path("asset_app/loan_asset/update/<int:pk>/", views.Loan_assetUpdateView.as_view(), name="asset_app_loan_asset_update"),
    path("asset_app/loaner_type/", views.Loaner_typeListView.as_view(), name="asset_app_loaner_type_list"),
    path("asset_app/loaner_type/create/", views.Loaner_typeCreateView.as_view(), name="asset_app_loaner_type_create"),
    path("asset_app/loaner_type/detail/<int:pk>/", views.Loaner_typeDetailView.as_view(), name="asset_app_loaner_type_detail"),
    path("asset_app/loaner_type/update/<int:pk>/", views.Loaner_typeUpdateView.as_view(), name="asset_app_loaner_type_update"),
    path("asset_app/locations/", views.LocationsListView.as_view(), name="asset_app_locations_list"),
    path("asset_app/locations/create/", views.LocationsCreateView.as_view(), name="asset_app_locations_create"),
    path("asset_app/locations/detail/<int:pk>/", views.LocationsDetailView.as_view(), name="asset_app_locations_detail"),
    path("asset_app/locations/update/<int:pk>/", views.LocationsUpdateView.as_view(), name="asset_app_locations_update"),
    path("asset_app/model/", views.ModelListView.as_view(), name="asset_app_model_list"),
    path("asset_app/model/create/", views.ModelCreateView.as_view(), name="asset_app_model_create"),
    path("asset_app/model/detail/<int:pk>/", views.ModelDetailView.as_view(), name="asset_app_model_detail"),
    path("asset_app/model/update/<int:pk>/", views.ModelUpdateView.as_view(), name="asset_app_model_update"),
    path("asset_app/room/", views.RoomListView.as_view(), name="asset_app_room_list"),
    path("asset_app/room/create/", views.RoomCreateView.as_view(), name="asset_app_room_create"),
    path("asset_app/room/detail/<int:pk>/", views.RoomDetailView.as_view(), name="asset_app_room_detail"),
    path("asset_app/room/update/<int:pk>/", views.RoomUpdateView.as_view(), name="asset_app_room_update"),
    path("asset_app/room_type/", views.Room_typeListView.as_view(), name="asset_app_room_type_list"),
    path("asset_app/room_type/create/", views.Room_typeCreateView.as_view(), name="asset_app_room_type_create"),
    path("asset_app/room_type/detail/<int:pk>/", views.Room_typeDetailView.as_view(), name="asset_app_room_type_detail"),
    path("asset_app/room_type/update/<int:pk>/", views.Room_typeUpdateView.as_view(), name="asset_app_room_type_update"),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.urls import path, include
from rest_framework import routers
from . import api
from . import views


router = routers.DefaultRouter()
router.register("locations", api.locationsViewSet)
router.register("asset_type", api.asset_typeViewSet)
router.register("loan_asset", api.loan_assetViewSet)
router.register("room", api.roomViewSet)
router.register("asset", api.assetViewSet)
router.register("loaner_type", api.loaner_typeViewSet)
router.register("model", api.modelViewSet)

urlpatterns = (
    path("api/v1/", include(router.urls)),
    path("asset_app/locations/", views.locationsListView.as_view(), name="asset_app_locations_list"),
    path("asset_app/locations/create/", views.locationsCreateView.as_view(), name="asset_app_locations_create"),
    path("asset_app/locations/detail/<int:pk>/", views.locationsDetailView.as_view(), name="asset_app_locations_detail"),
    path("asset_app/locations/update/<int:pk>/", views.locationsUpdateView.as_view(), name="asset_app_locations_update"),
    path("asset_app/asset_type/", views.asset_typeListView.as_view(), name="asset_app_asset_type_list"),
    path("asset_app/asset_type/create/", views.asset_typeCreateView.as_view(), name="asset_app_asset_type_create"),
    path("asset_app/asset_type/detail/<int:pk>/", views.asset_typeDetailView.as_view(), name="asset_app_asset_type_detail"),
    path("asset_app/asset_type/update/<int:pk>/", views.asset_typeUpdateView.as_view(), name="asset_app_asset_type_update"),
    path("asset_app/loan_asset/", views.loan_assetListView.as_view(), name="asset_app_loan_asset_list"),
    path("asset_app/loan_asset/create/", views.loan_assetCreateView.as_view(), name="asset_app_loan_asset_create"),
    path("asset_app/loan_asset/detail/<int:pk>/", views.loan_assetDetailView.as_view(), name="asset_app_loan_asset_detail"),
    path("asset_app/loan_asset/update/<int:pk>/", views.loan_assetUpdateView.as_view(), name="asset_app_loan_asset_update"),
    path("asset_app/room/", views.roomListView.as_view(), name="asset_app_room_list"),
    path("asset_app/room/create/", views.roomCreateView.as_view(), name="asset_app_room_create"),
    path("asset_app/room/detail/<int:pk>/", views.roomDetailView.as_view(), name="asset_app_room_detail"),
    path("asset_app/room/update/<int:pk>/", views.roomUpdateView.as_view(), name="asset_app_room_update"),
    path("asset_app/asset/", views.assetListView.as_view(), name="asset_app_asset_list"),
    path("asset_app/asset/create/", views.assetCreateView.as_view(), name="asset_app_asset_create"),
    path("asset_app/asset/detail/<int:pk>/", views.assetDetailView.as_view(), name="asset_app_asset_detail"),
    path("asset_app/asset/update/<int:pk>/", views.assetUpdateView.as_view(), name="asset_app_asset_update"),
    path("asset_app/loaner_type/", views.loaner_typeListView.as_view(), name="asset_app_loaner_type_list"),
    path("asset_app/loaner_type/create/", views.loaner_typeCreateView.as_view(), name="asset_app_loaner_type_create"),
    path("asset_app/loaner_type/detail/<int:pk>/", views.loaner_typeDetailView.as_view(), name="asset_app_loaner_type_detail"),
    path("asset_app/loaner_type/update/<int:pk>/", views.loaner_typeUpdateView.as_view(), name="asset_app_loaner_type_update"),
    path("asset_app/model/", views.modelListView.as_view(), name="asset_app_model_list"),
    path("asset_app/model/create/", views.modelCreateView.as_view(), name="asset_app_model_create"),
    path("asset_app/model/detail/<int:pk>/", views.modelDetailView.as_view(), name="asset_app_model_detail"),
    path("asset_app/model/update/<int:pk>/", views.modelUpdateView.as_view(), name="asset_app_model_update"),
)

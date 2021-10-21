from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.UploadView.as_view(), name='upload'),
    path('explore/', views.BuildingList.as_view(), name='explore'),
    path('explore/building/<int:building_id>', views.MeterList.as_view(), name='explore_building'),
    path('explore/meter/<int:meter_id>', views.MeterReadingsList.as_view(), name='explore_meter'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('admin/', admin.site.urls)
]

router = DefaultRouter()
router.register('building', views.BuildingViewSet, basename='building')
router.register('fuel', views.FuelViewSet, basename='fuel')
router.register('meter', views.MeterViewSet, basename='meter')
router.register('meter_reading', views.MeterReadingViewSet, basename='meter_reading')

urlpatterns += router.urls

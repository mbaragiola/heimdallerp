from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from geo import views

router = DefaultRouter()
router.register(r'alternativenames', views.AlternativeNameViewSet)
router.register(r'districts', views.DistrictViewSet)
router.register(r'cities', views.CityViewSet)
router.register(r'subregions', views.SubregionViewSet)
router.register(r'regions', views.RegionViewSet)
router.register(r'countries', views.CountryViewSet)

app_name = 'geo'
urlpatterns = [
    url(
        r'^countries/(?P<pk>\d+)/regions/$',
        views.RegionsByCountryList.as_view(),
        name='country-regions'
    ),
    url(
        r'^countries/(?P<pk>\d+)/cities/$',
        views.CitiesByCountryList.as_view(),
        name='country-cities'
    ),
    url(
        r'^regions/(?P<pk>\d+)/cities/$',
        views.CitiesByRegionList.as_view(),
        name='region-cities'
    ),
    url(
        r'^regions/(?P<pk>\d+)/subregions/$',
        views.SubregionsByRegionList.as_view(),
        name='region-subregions'
    ),
    url(
        r'^cities/(?P<pk>\d+)/districts/$',
        views.DistrictsByCityList.as_view(),
        name='city-districts'
    ),
    url(r'^', include(router.urls)),
]

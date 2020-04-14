from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital


urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addhospital',GetDistrictByState.as_view(),name='addhospital'),
        ]

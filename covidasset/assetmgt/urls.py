from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital
from assetmgt.hospitalviews import AddMultipleHospital
from assetmgt.hospitalviews import GetHospitalSample 


urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
        path('gethospitalsamplecsv',GetHospitalSample.as_view(),name='gethospitalsample'),
        path('addhospitalcsv',AddMultipleHospital.as_view(),name='addhospitalcsv'),

        ]

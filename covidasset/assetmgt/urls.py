from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate


urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        ]

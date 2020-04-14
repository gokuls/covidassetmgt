"""covidasset URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path

from assetmgt import usercreation
#from assetmgt import hospital
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usercreation.index, name="index"),
    path('adduser', usercreation.register, name="register"),
    path('addhospital', usercreation.addHospital, name="addhospital"),
    path('ajax/load-dist/', usercreation.load_district, name='ajax_load_districts'),
    path('ajax/load-hospital/', usercreation.load_hospital, name='ajax_load_hospital'),
#K.Karthikeyan
#    path('add_hospital',hospital.addHospital,name="add_hospital"),
    path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
    path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
]

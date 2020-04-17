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
from django.urls import include

from django.urls import path
from django.urls import re_path

from assetmgt import usercreation
from assetmgt import assetmgt

#from assetmgt import hospital
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', usercreation.index, name="index"),
    path('adduser', usercreation.register, name="register"),
    path('addhospital', usercreation.addHospital, name="addhospital"),
    ## asset management
    path('assets', assetmgt.AssetsView, name="assetview"),
    path('assetmanagement', assetmgt.AssetManagementView, name="assetmanagementview"),
    path('assetmanagementimg', assetmgt.AssetManagementImgView, name="assetmanagementimgview"),
    path('ajax/load-dist/', usercreation.load_district, name='ajax_load_districts'),
    path('assetmgt/',include('assetmgt.urls'),name='assetmgt'),
    path('ajax/load-hospital/', usercreation.load_hospital, name='ajax_load_hospital'),
    path('ajax/loadassetform/', assetmgt.returnAssetForm, name='assetcform'),
    path('ajax/loadassetmgtform/', assetmgt.returnAssetMgtForm, name='assetmgtform'),
    path('ajax/loadallastform/', assetmgt.returnAssetMgtMultiForm, name='assetmgtmultiforms'),
    path('ajax/loadassetimg/', assetmgt.returnAssetShow, name='assetshow'),
    path('addasset/', assetmgt.addAsset, name='addasset'),
    path('ajax/addentry/', assetmgt.addAssetManagement, name='addassetmanagement'),
    path('ajax/addmulentry/', assetmgt.addMultipleAssetManagement, name='addmultiassetmanagement'),
    path('login', assetmgt.LoginMeth, name='login'),
    #path('', assetmgt.LoginMeth, name='login1'),
    path('logout', assetmgt.Logout_view, name='logout'),
]

from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital
from assetmgt.hospitalviews import AddMultipleHospital
from assetmgt.hospitalviews import GetHospitalSample,GetHospitalData
from assetmgt.hospitalviews import GetHospitalSample 
from assetmgt.assetreport import GetReport 
from assetmgt import assetreport
from .views import AssetFileUploadView
from django.conf import settings
from django.conf.urls.static import static
from assetmgt import apiviews as apicall

urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
        path('assetfileupload',AssetFileUploadView.as_view(),name='assetfileupload'),
        path('gethospitalsamplecsv',GetHospitalSample.as_view(),name='gethospitalsample'),
        path('addhospitalcsv',AddMultipleHospital.as_view(),name='addhospitalcsv'),
        path('gethospitaldata',GetHospitalData.as_view(),name='gethospitaldata'),
        path('assetreport',assetreport.assetReport,name='assetreport'),
        path('generatereport',GetReport.as_view(),name='generatereport'),
        #Apiurls
        path('getallState',apicall.getAllState,name='getallstate'),
        path('totalcounts',apicall.getTotalCounts,name='totalcounts'),
        #path('getstatedata',apicall.getState,name='getstatedata'),
        path('getstatedata',apicall.getStateNew,name='getstatedata'),
        path('getdistrictdata',apicall.getHospitalsByDistrict,name='getdistrictdata'),
        path('getstatenamebyid',apicall.getStateNameById,name='getstatenamebyid'),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        

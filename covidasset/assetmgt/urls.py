from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital
from assetmgt.hospitalviews import AddMultipleHospital, UploadHospitalXls
from assetmgt.hospitalviews import GetHospitalSample,GetHospitalData
from assetmgt.hospitalviews import GetHospitalSample
from assetmgt.hospitalviews import hospitalxlsGenerate
from assetmgt.assetreport import GetReport 
from assetmgt import assetreport
from assetmgt import hospitalsearch
from .views import AssetFileUploadView
from django.conf import settings
from django.conf.urls.static import static
from assetmgt import apiviewsv2 as apicall

urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
        path('assetfileupload',AssetFileUploadView.as_view(),name='assetfileupload'),
        path('gethospitalsamplefcsv',GetHospitalSample.as_view(),name='gethospitalsample'),
        path('gethospitalxls',hospitalxlsGenerate,name='gethospitalxls'),
        path('addhospitalcsv',AddMultipleHospital.as_view(),name='addhospitalcsv'),
        path('uploadhospitalxls',UploadHospitalXls.as_view(),name='uploadhospitalxls'),        
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
        path('gethospitaltype',apicall.getHospitalType,name='gethospitaltype'),
        
        #For hospital search by assets(by patient)
        path('getallstates',hospitalsearch.get_all_states,name='getallstates'),
        path('getalldistrictsbystate',hospitalsearch.get_all_districts_by_state,name='getalldistrictsbystate'),
        path('getallassets',hospitalsearch.get_all_assets,name='getallassets'),
        path('gethospitalasset',hospitalsearch.get_hospitals_with_assets,name='gethospitalasset'),
        ]
        

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        

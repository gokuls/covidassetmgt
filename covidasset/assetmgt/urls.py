from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital
from assetmgt.hospitalviews import AddMultipleHospital
<<<<<<< HEAD
from assetmgt.hospitalviews import GetHospitalSample,GetHospitalData

=======
from assetmgt.hospitalviews import GetHospitalSample 
from assetmgt import assetreport
>>>>>>> 1bf94b76ee94f6f78015e4e82c9821dc5c48bf8e

from .views import AssetFileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
        path('assetfileupload',AssetFileUploadView.as_view(),name='assetfileupload'),
        path('gethospitalsamplecsv',GetHospitalSample.as_view(),name='gethospitalsample'),
        path('addhospitalcsv',AddMultipleHospital.as_view(),name='addhospitalcsv'),
        path('gethospitaldata',GetHospitalData.as_view(),name='gethospitaldata'),
        path('assetreport',assetreport.assetReport,name='assetreport'),
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        

from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital
from assetmgt.hospitalviews import AddMultipleHospital
from assetmgt.hospitalviews import GetHospitalSample 


from .views import AssetFileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
<<<<<<< HEAD
        path('assetfileupload',AssetFileUploadView.as_view(),name='assetfileupload'),
        
=======
        path('gethospitalsamplecsv',GetHospitalSample.as_view(),name='gethospitalsample'),
        path('addhospitalcsv',AddMultipleHospital.as_view(),name='addhospitalcsv'),

>>>>>>> 3bb370fa67daae502208cae628c3e6f24d055285
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        
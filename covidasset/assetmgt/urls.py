from django.urls import path,re_path,include
from assetmgt.hospitalviews import AddHospitalTemplate
from assetmgt.hospitalviews import GetDistrictByState
from assetmgt.hospitalviews import AddHospital


from .views import AssetFileUploadView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
        path('addhospitaltemp',AddHospitalTemplate.as_view(),name='addhospitaltemp'),
        path('getdistrict',GetDistrictByState.as_view(),name='getdistrict'),
        path('addsinglehospital',AddHospital.as_view(),name='addsinglehospital'),
        path('assetfileupload',AssetFileUploadView.as_view(),name='assetfileupload'),
        
        ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        
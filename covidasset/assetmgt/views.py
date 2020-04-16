from django.shortcuts import render
from django.http import Http404
from .forms import AssetFilesForm

from .models import AssetFiles
from .models import AssetMgt
from .models import Hospital
from .models import Asset

from django.views import View
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

import time
import xlrd

# Create your views here.

class AssetFileUploadView(View):
     
    def post(self, request):
        if request.FILES['datafile']:
            print('File Objects True')
            myfile = request.FILES['datafile']
            fs = FileSystemStorage()
            
            #FileName with EPOC time format
            epoc=int(time.time())
            tmpfileName = str(request.user)+"-"+str(epoc)+".csv"
            filename = fs.save(tmpfileName, myfile)
            
            # Models Saved 
            af = AssetFiles()
            af.file_name=tmpfileName
            af.datafile=fs.url(filename)
            af.save()

            # AssetMgmt List Constructions and saved to database           

            wb=xlrd.open_workbook(settings.MEDIA_ROOT+"/"+filename)
            sheet=wb.sheet_by_index(0)
            for row in range(1,(sheet.nrows)):
                ad = AssetMgt()                
                ad.hospital_id=Hospital.objects.get(hospital_id=int(sheet.cell_value(row,0)))
                ad.asset_id=Asset.objects.get(asset_id=int(sheet.cell_value(row,1)))
                ad.asset_total=int(sheet.cell_value(row,2))
                ad.asset_utilized=int(sheet.cell_value(row,3))
                ad.asset_balance=ad.asset_total-ad.asset_utilized
                ad.save()

            ## Successful Message
            messages.info(request,"File Uploaded Successfully")
            url = reverse('assetmanagementview')
            return HttpResponseRedirect(url)
        else:
            messages.info(request,"File Not Uploaded")
            url = reverse('assetmanagementview')
            return HttpResponseRedirect(url)

           
        

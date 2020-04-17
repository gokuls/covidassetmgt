from django.shortcuts import render
from django.http import Http404
from .forms import AssetFilesForm

from .models import AssetFiles
from .models import AssetMgt
from .models import Hospital
from .models import Asset

from django.db import transaction

from django.views import View
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.http import  HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

import time
import xlrd
import xlwt
import os

# Create your views here.

class AssetFileUploadView(View):
     
    def post(self, request):
        if request.FILES['datafile']:            
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
            try:
                wb=xlrd.open_workbook(settings.MEDIA_ROOT+"/"+filename)
                sheet=wb.sheet_by_index(0)
                with transaction.atomic():
                    for row in range(1,(sheet.nrows)):
                        ad = AssetMgt()                
                        ad.hospital_id=Hospital.objects.get(hospital_id=int(sheet.cell_value(row,0)))
                        ad.asset_id=Asset.objects.get(asset_name=str(sheet.cell_value(row,2)))
                        ad.asset_total=int(sheet.cell_value(row,3))
                        ad.asset_utilized=int(sheet.cell_value(row,4))
                        ad.asset_balance=ad.asset_total-ad.asset_utilized
                        ad.save()
                 ## Successful Message
                messages.info(request,"File Uploaded Successfully")
                url = reverse('assetmanagementview')
                return HttpResponseRedirect(url)
            except Exception as e:
                messages.error(request,"Record Not Saved !!! Check the value in the File")
                url = reverse('assetmanagementview')
                return HttpResponseRedirect(url)           
        else:
            messages.info(request,"File Not Uploaded")
            url = reverse('assetmanagementview')
            return HttpResponseRedirect(url)


def xlsGenerate(assetmt, username):
    wb = xlwt.Workbook() # create empty workbook object
    newsheet = wb.add_sheet('asset_details') # sheet name can not be longer than 32 characters
    
    newsheet.write(0,0,'hospital_id') 
    newsheet.write(0,1,'hospital_name')
    newsheet.write(0,2,'Asset_name')
    newsheet.write(0,3,'Total')
    newsheet.write(0,4,'Utilized')

    rows=1
    for asset in assetmt:
        newsheet.write(rows,0,asset.hospital_id.hospital_id)
        newsheet.write(rows,1,asset.hospital_id.hospital_name) 
        newsheet.write(rows,2,asset.asset_id.asset_name) 
        newsheet.write(rows,3,asset.asset_total) 
        newsheet.write(rows,4,asset.asset_utilized)
        rows += 1 

    
    #tmpfileName = settings.MEDIA_ROOT+"/tmp/"+"tmp-"+username+".xls"
    destFolder = os.path.join(settings.BASE_DIR,'assetmgt/static/assetmgt/temp')
    tmpfileName = os.path.join(destFolder,'tmp-%s.xls'%username)
    murl = "assetmgt/temp/tmp-%s.xls"%username
    wb.save(tmpfileName)
    return murl



           
        

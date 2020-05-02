from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse,FileResponse
from django.http import StreamingHttpResponse

from django.views.generic import View,TemplateView,ListView
from django.views.decorators.csrf import csrf_exempt
#from assetmgt.hospitalforms import HospitalForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings 
import os
import sys
import csv
import xlrd
import xlwt
import time
from  django.db.utils import IntegrityError
from django.urls import reverse
from django.http import  HttpResponseRedirect

from django.core.files.storage import FileSystemStorage

from assetmgt.models import (Hospital,
        Asset,
        State,
        District,
        AssetMgt,
        UserProfile,
        HospitalType,
        HtypeAssetMapping,
        HospAssetMapping)

htypes_header = HospitalType.objects.all().values_list('hospital_type',flat=True)
DATA_CSV_HEADER = [ "District",
        "Hospital_Name",
        "Hospital_Type("+'/'.join(htypes_header)+")",
        "FullAddress",
        "City",
        "Taluk",
        "PINCODE",
        "Phone_Number(with STD-code)",
        "Total_Doctors",
        "Total_HealthWorkers" ]

class AddHospitalTemplate(LoginRequiredMixin,View):
    '''To render a templet to get hospital Information Invidually '''
    login_url = 'login'
    def get(self,request):
        #To do user username from request object
        context_dict = {}
        print("User----------",request.user.username)
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)
            states = State.objects.filter(state_name=usr.state_id)#To do to query the State respect to the user permission
            context_dict['usr'] = usr
            htypes = HospitalType.objects.all()
        except UserProfile.DoesNotExist as usr_profile_not_found:
            print("exception while checking user profile %s"%(usr_profile_not_found))
            states = State.objects.all()#To do to query the State respect to the user permission
        #assets = Asset.objects.all()
        context_dict['states'] = states
        context_dict['htype'] = htypes
        return render(request,'assetmgt/add_hospital.html',context=context_dict)


class GetDistrictByState(View):

    def post(self,request):
        stateid = int(request.POST['stateid'])#To do verify stateid mapped in UserProfile also
        districts = {}
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)
            if usr.adminstate == 2:
                state = State.objects.get(pk=stateid)
                districts = District.objects.filter(state_id=state)
            else:
                districts = District.objects.filter(state_id=usr.state_id.state_id,
                    district_id=usr.district_id.district_id)
            print(districts)
        except State.DoesNotExist as state_not_found:
            print(state_not_found)
            
        return render(request,"assetmgt/district_dropdown_list.html",{'dist':districts})
            

class AddHospital(LoginRequiredMixin,View):
    login_url = 'login'
    #@transaction.atomic
    def post(self,request):
        #usr = User.objects.get(username='boss')
        #To do user username from request object
        #if not request.user:
        assets = Asset.objects.all()

        usr = UserProfile.objects.get(user__username=request.user.username)
        #To do user username from request object
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)#To do user username from request object
            states = State.objects.filter(state_name=usr.state_id)#To do to query the State respect to the user permission
            htypes = HospitalType.objects.all()
        except UserProfile.DoesNotExist as e:
            print("exception while add hospital %s"%(str(e)))
            states = State.objects.all()

        try:
            #To do get user's distict,state ids 
            htv = request.POST['htype']
            try:
                htobj = HospitalType.objects.get(htype_id=int(htv))
                ht = htobj.hospital_type
                htyp = htobj
            except Exception as details:
                ht = htv
                htyp = htv

            stid = int(request.POST['state'])  
            did = int(request.POST['district'])
            tk = request.POST['taluk']
            city = request.POST['city']
            addr = request.POST['haddress']
            pin = request.POST['hpin']
            #ht = request.POST['htype']
            nd = int(request.POST['ndoc'])
            nhw = int(request.POST['nhw'])
            hcontact = request.POST['hcontact']
            hname = request.POST['hname']
            opt = int(request.POST['opt'])
            #To get State and District Objects
            s = State.objects.get(state_id=stid)
            d = District.objects.get(district_id=did)
            if opt == 0:
                with transaction.atomic():
                    hospital_obj = Hospital.objects.create(
                        state_id=s,district_id=d,hospital_name=hname,
                        hospital_type=ht,city=city,taluk=tk,address=addr,
                        contact_number=hcontact,pincode=pin,doctors=nd,
                        healthworkers=nhw,htype=htyp)
                    htype_mapping_obj = HtypeAssetMapping.objects.filter(htype=hospital_obj.htype).select_related('assetsmapped')
                    for htype_asset in htype_mapping_obj:
                        HospAssetMapping.objects.create(hospital=hospital_obj,assetsmapped=htype_asset.assetsmapped)
 
                    messages.info(request,hname+" added successfully") 
                    # for asset in assets:
                    #     AssetMgt.objects.create(asset_id=asset,
                    #         hospital_id=hospital_obj,
                    #         author=usr.user,
                    #         asset_total=0,asset_utilized=0,
                    #         asset_balance=0)
            else:
                with transaction.atomic():
                    hid = int(request.POST['hid'])
                    h = Hospital.objects.get(hospital_id=hid)
                    h.hospital_name = hname
                    h.hospital_type=ht
                    h.city = city
                    h.taluk = tk
                    h.address = addr
                    h.contact_number = hcontact
                    h.doctors = nd
                    h.healthworkers = nhw
                    h.pincode = pin
                    h.htype=htyp
                    h.save()
                    htype_mapping_obj = HtypeAssetMapping.objects.filter(htype=hospital_obj.htype).select_related('assetsmapped')
                    for htype_asset in htype_mapping_obj:
                        HospAssetMapping.objects.create(hospital=hospital_obj,assetsmapped=htype_asset.assetsmapped)
 
                    messages.info(request,hname+" details updated successfully")
                    print("hospital updated")

        except Exception as add_h_err:
            print("exception in adding single hospital %s"%(str(add_h_err)))
            messages.error(request,hname+" not added")
        print("Printing htype ")
        print(htypes)
        return render(request,'assetmgt/add_hospital.html',
            {'states':states,'usr':usr,'htype':htypes
            })


class GetHospitalSample(View):
    def get(self,request):
        dir_name = settings.MEDIA_ROOT
        extendsion = ".csv"
        sample_file = os.path.join(dir_name,"sample","sample_hospital.csv")
        statobj = os.stat(sample_file)
        usr = UserProfile.objects.get(user__username=request.user.username)
        state_name = usr.state_id.state_name
        district_name = usr.district_id.district_name
        #assets_list = Asset.objects.all().values_list('asset_name',flat=True)
        #asset_names = list(map(lambda x: "Total_"+x+"_available",assets_list))
        adminstate = usr.adminstate
        htypes = HospitalType.objects.all().values_list('hospital_type',flat=True)
        sample_data = [' ',' ',' ',' ',' ',' ',' ',' ',' '] 
        global DATA_CSV_HEADER
        if adminstate == 1:
            title_row = DATA_CSV_HEADER[1:]
        elif adminstate == 2:
            title_row = DATA_CSV_HEADER 

        else:
            title_row = list()

        #title_row.extend(asset_names)
        print(title_row)
        sample_csv = open(sample_file,"w")
        sample_csv.write(",".join(title_row))
        if adminstate == 2:
            districts = District.objects.filter(state_id=usr.state_id).values_list('district_name',flat=True)
            for district in districts:
                sample_data[0]=district
                sample_data[2]='/'.join(htypes)
                sample_csv.write("\n"+",".join(sample_data))
        else:
            sample_data[2]= '/'.join(htypes)
            sample_csv.write("\n"+",".join(sample_data))

        sample_csv.close()
        response = FileResponse(open(sample_file,"rb"))
        #response = HttpResponse(mimetype='application/force-download')
        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = statobj.st_size
        response['Content-Disposition'] = 'attachment; filename=%s'%(os.path.basename(sample_file))
        #response['Content-Disposition'] = 'attachment; filename=hospital_uploadtemplate.xls'
        return response
        
        


class AddMultipleHospital(LoginRequiredMixin,View):
    login_url = 'login'

    def validate_values(self,values_dict):
        if values_dict[DATA_CSV_HEADER[1]].isspace() or values_dict[DATA_CSV_HEADER[3]].isspace() or values_dict[DATA_CSV_HEADER[4]].isspace() or values_dict[DATA_CSV_HEADER[5]].isspace() or values_dict[DATA_CSV_HEADER[6]].isspace() or values_dict[DATA_CSV_HEADER[7]].isspace() or values_dict[DATA_CSV_HEADER[8]].isalpha() or values_dict[DATA_CSV_HEADER[9]].isspace() or values_dict[DATA_CSV_HEADER[9]].isalpha():
            return False
        else:
            return True

    def post(self,request):
        states = State.objects.all()
        assets = Asset.objects.all()
        usr = UserProfile.objects.get(user__username=request.user.username)
        field_name_list = list()
        try:
            #usr = UserProfile.objects.get(user__username=request.user.username)
            state_obj = usr.state_id
            states = State.objects.filter(state_name=state_obj)
            district_obj = usr.district_id
            myfile = request.FILES['datafile']
            print("---------------------",myfile.name)
            filename = myfile.name
            #Check uploaded file extention is csv
            if not filename.endswith('.csv'):
                messages.error(request,"Only .csv file allowed, Uploaded file is not csv file")
                return render(render,'assetmgt/add_hospital.html',{'states':states,'usr':usr})

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            #print("File save in "+str(uploaded_file_url))
            file_path = os.path.join(settings.MEDIA_ROOT,filename)
            #print("File path is "+file_path)
            global DATA_CSV_HEADER
            #if os.path.isfile(file_path) and os.path.exists(file_path)
            if usr.adminstate == 2:
                field_name_list = DATA_CSV_HEADER
            else:
                field_name_list = DATA_CSV_HEADER[1:]

            data = csv.DictReader(open(file_path),fieldnames=field_name_list)
            #print("Data-----",dir(data))
            #print("number of lines ",data.line_num)
            for row in data:
                #print("Row->",row)
                header = ','.join(row.values())
                field_count = len(row.values())
                
                if field_count < 8:
                    messages.error(request,"Some data could be missed  in record about "+"-".join(row.values()))
                    continue
                dheader = ','.join(DATA_CSV_HEADER)
                #print(header)
                #print(dheader)
                if usr.adminstate == 2:
                    #print(usr.adminstate)
                    try:
                        if not self.validate_hospital_data(row[DATA_CSV_HEADER[1]],row[DATA_CSV_HEADER[7]],row[DATA_CSV_HEADER[6]]):
                            messages.error(request,"Hospital data already exists "+",".join(row.values()))
                            continue

                        if not self.validate_values(row):
                            messages.error(request,"Hospital data may have invalid format "+",".join(row.values()))
                            continue

                        if not self.validate_hospital_type(row[DATA_CSV_HEADER[2]]):
                            messages.error(request,"Invalid Hospital type "+",".join(row.values()))
                            continue

                        districtname = row[DATA_CSV_HEADER[0]]

                        with transaction.atomic():
                            hospital_obj = Hospital.objects.create(
                                    state_id=state_obj,
                                    district_id=District.objects.get(district_name=districtname),
                                    hospital_name=row[DATA_CSV_HEADER[1]],
                                    hospital_type=row[DATA_CSV_HEADER[2]],
                                    city=row[DATA_CSV_HEADER[4]],
                                    taluk=row[DATA_CSV_HEADER[5]],
                                    address=row[DATA_CSV_HEADER[3]],
                                    contact_number=row[DATA_CSV_HEADER[7]],
                                    pincode=row[DATA_CSV_HEADER[6]],
                                    doctors=int(row[DATA_CSV_HEADER[8]]),
                                    healthworkers=int(row[DATA_CSV_HEADER[9]]),
                                    htype = HospitalType.objects.get(hospital_type=row[DATA_CSV_HEADER[2]])
                                    )
                            htype_mapping_obj = HtypeAssetMapping.objects.filter(htype=hospital_obj.htype).select_related('assetsmapped')
                            for htype_asset in htype_mapping_obj:
                                HospAssetMapping.objects.create(hospital=hospital_obj,assetsmapped=htype_asset.assetsmapped)
                            for asset in htype_mapping_obj:
                                AssetMgt.objects.create(asset_id=asset.assetsmapped,hospital_id=hospital_obj,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0) 
                            messages.info(request,hospital_obj.hospital_name+" Hospital Added successfully")
                    except District.DoesNotExist as district_nod_found:
                        messages.error(request,"Uploaded file having invalid data "+",".join(row.values()))
                        continue

                    except ValueError as ver:
                        messages.error(request,"Uploaded file having invalid data for numerical values as \n "+",".join(row.values()))
                        continue

                else:
                    dheader = ','.join(DATA_CSV_HEADER[1:])
                    if header == dheader:
                        continue

                    if not self.validate_hospital_data(row[DATA_CSV_HEADER[1]],row[DATA_CSV_HEADER[7]],row[DATA_CSV_HEADER[6]]):
                        messages.error(request,"Hospital data already exists "+",".join(row.values()))
                        continue                    

                    if not self.validate_values(row):
                        print(row)
                        messages.error(request,"Hospital data may have invalid format "+",".join(row.values()))
                        continue
                            
                    if not self.validate_hospital_type(row[DATA_CSV_HEADER[2]]):
                        messages.error(request,"Invalid Hospital type "+",".join(row.values()))
                        continue

                    with transaction.atomic():
                        hospital_obj = Hospital.objects.create(
                                state_id=state_obj,
                                district_id=district_obj,
                                hospital_name=row[DATA_CSV_HEADER[1]],
                                hospital_type=row[DATA_CSV_HEADER[2]],
                                city=row[DATA_CSV_HEADER[4]],
                                taluk=row[DATA_CSV_HEADER[5]],
                                address=row[DATA_CSV_HEADER[3]],
                                contact_number=row[DATA_CSV_HEADER[7]],
                                pincode=row[DATA_CSV_HEADER[6]],
                                doctors=int(row[DATA_CSV_HEADER[8]]),
                                healthworkers=int(row[DATA_CSV_HEADER[9]]),
                                htype = HospitalType.objects.get(hospital_type=row[DATA_CSV_HEADER[2]])
                                )
                        htype_mapping_obj = HtypeAssetMapping.objects.filter(htype=hospital_obj.htype).select_related('assetsmapped')
                        for htype_asset in htype_mapping_obj:
                            HospAssetMapping.objects.create(hospital=hospital_obj,assetsmapped=htype_asset.assetsmapped)

                        for asset in htype_mapping_obj:
                            AssetMgt.objects.create(asset_id=asset.assetsmapped,hospital_id=hospital_obj,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0) 
                        messages.info(request,hospital_obj.hospital_name+" Hospital Added successfully")

        except Exception as er3:
            print("Exception while add multiple hospital ",er3)
            messages.error(request,"Hospital Data be in-correct format or order,Please use sample csv format")

        return render(request,'assetmgt/add_hospital.html',{'states':states,'usr':usr})

    def validate_hospital_data(self,hname,hphone,hpincode):
        ''' To valiidate hospital data while add hospital '''
        try:
            hobj = Hospital.objects.get(hospital_name=hname)
            if hobj:
                if hphone == hobj.contact_number:
                    return False
                
        except Hospital.DoesNotExist as er:
            print("*********",er)
            return True
        except Exception as ser:
            print("===============",ser)
            return False

    def validate_hospital_type(self,htype):
        '''To validate validate hospital type '''
        try:
            ht = HospitalType.objects.get(hospital_type=htype)
            if ht:
                return True
        except HospitalType.DoesNotExist as invalid:
            print(invalid)
            return False

        except Exception as er:
            print(er)
            return False




class GetHospitalData(View):
    def post(self,request):
        data = {}
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)
            h_data = Hospital.objects.filter(hospital_id=usr.hospital_id.hospital_id,state_id__state_id=usr.state_id.state_id,district_id__district_id=usr.district_id.district_id).values('hospital_id','state_id','district_id','hospital_name', 'hospital_type','city','taluk','address','pincode','doctors','healthworkers','contact_number')
            print(h_data)
            if h_data.exists():
                data = h_data[0]
                district_name = District.objects.get(district_id=data['district_id']).district_name
                data['dist_name'] = district_name
        except Exception as get_h_data:
            print("exception while getting hospital data %s"%(str(get_h_data)))

        return JsonResponse(data)
            



class IndexPage(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = 'not logged in'

        context = {'user':user}
        return render(request,'assetmgt/index-new-1.html',context)


#==================== K. Karthikeyan =====================================
class UploadHospitalXls(LoginRequiredMixin,View):
    login_url = 'login'
    
    def post(self,request):
        if request.FILES['datafile']:            
            myfile = request.FILES['datafile']
            fs = FileSystemStorage()
            
            #FileName with EPOC time format
            epoc=int(time.time())
            tmpfileName = str(request.user)+"-"+str(epoc)+".csv"
            filename = fs.save(tmpfileName, myfile)
            user = UserProfile.objects.get(user__username=request.user.username)
            
            try:
                wb=xlrd.open_workbook(settings.MEDIA_ROOT+"/"+filename)
                sheet=wb.sheet_by_index(0)
                with transaction.atomic():
                    for row in range(1,(sheet.nrows)):
                        #If total value is 0 Fields is Ommited
                        """balance = sheet.cell_value(row,3) - sheet.cell_value(row,4)                        
                        if sheet.cell_value(row,3) == 0 :
                            continue
                        elif balance < 0:
                            raise Exception('Value Error for {}, Check Value of Assets'.format(sheet.cell_value(row,1)))"""                     
                        hospital = Hospital()                
                        hospital.state_id=user.state_id
                        hospital.district_id=District.objects.get(district_name=str(sheet.cell_value(row,0)))                                            
                        hospital.district_id=District.objects.get(district_name=str(sheet.cell_value(row,0)))                                            
                        hospital.hospital_name = str(sheet.cell_value(row,1))
                        if len(hospital.hospital_name) == 0:
                            raise Exception('Value Error for {}, Check Value Hospitalname'.format(sheet.cell_value(row,1)))
                        hospital.htype=HospitalType.objects.get(hospital_type=str(sheet.cell_value(row,2)))
                        hospital.address=str(sheet.cell_value(row,3))
                        hospital.city=str(sheet.cell_value(row,4))
                        hospital.taluk=str(sheet.cell_value(row,5))
                        hospital.pincode=str(sheet.cell_value(row,6))
                        hospital.contact_number=str(sheet.cell_value(row,7))
                        hospital.latitude=str(sheet.cell_value(row,8))
                        hospital.longitude=str(sheet.cell_value(row,9))
                        hospital.doctors=int(sheet.cell_value(row,10))
                        hospital.healthworkers=int(sheet.cell_value(row,11))
                        hospital.save()

                        htype_mapping_obj = HtypeAssetMapping.objects.filter(htype=hospital.htype).select_related('assetsmapped')
                        for htype_asset in htype_mapping_obj:
                            HospAssetMapping.objects.create(hospital=hospital,assetsmapped=htype_asset.assetsmapped)
                        for asset in htype_mapping_obj:
                            AssetMgt.objects.create(asset_id=asset.assetsmapped,hospital_id=hospital,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0) 
                        print("Hospital ",hospital.hospital_name," Added successfully")    
                 ## Successful Message
                messages.info(request,"File Uploaded Successfully")
                url = reverse('addhospitaltemp')
                return HttpResponseRedirect(url)
            except Exception as e:                
                if isinstance(e, IntegrityError):
                    messages.error(request,'Constrain violation, Check Value of Assets')
                elif isinstance(e, ValueError):
                    messages.error(request,'Value Error, Check Value of Doctors, Healthworkers')
                else:
                    messages.error(request,str(e))
                    
                url = reverse('addhospitaltemp')
                return HttpResponseRedirect(url)           
        else:
            messages.info(request,"File Not Uploaded")
            url = reverse('addhospitaltemp')
            return HttpResponseRedirect(url)
    

def hospitalxlsGenerate(request):
    htypes = HospitalType.objects.all().values_list('hospital_type',flat=True)
    user = UserProfile.objects.get(user__username=request.user.username)
    
    wb = xlwt.Workbook() # create empty workbook object
    newsheet = wb.add_sheet('hospital_template') # sheet name can not be longer than 32 characters    
    newsheet1 = wb.add_sheet('Districts and Hospital Types') # sheet name can not be longer than 32 characters    
    newsheet.write(0,0,'District')
    newsheet1.write(0,0,'District') 

    newsheet.write(0,1,'Hospital_Name')
    newsheet.write(0,2,'Hospital_Type')    
    newsheet1.write(0,2,'Hospital_Type')
    newsheet.write(0,3,'Full Address')
    newsheet.write(0,4,'City')
    newsheet.write(0,5,'Taluk')
    newsheet.write(0,6,'Pincode')
    newsheet.write(0,7,'Contact_Number')
    newsheet.write(0,8,'latitude')
    newsheet.write(0,9,'longitude')
    newsheet.write(0,10,'Doctors')
    newsheet.write(0,11,'Health Workers')
    
    
    if user.adminstate == 2:
        dists = District.objects.filter(state_id=user.state_id).values_list("district_name",flat=True)
        i = 1
        for dist in dists:
            newsheet1.write(i,0,dist)
            i+=1

    if user.adminstate == 1:
        dist = user.district_id.district_name 
        newsheet1.write(1,0,dist)
    
    i = 1
    for htype in htypes:
        newsheet1.write(i,2,htype)
        i+=1
  
  
    #if settings.DEBUG:
    try:
        if (sys.argv[1] == 'runserver'):            
            destFolder = os.path.join(settings.BASE_DIR,'assetmgt/static/assetmgt/temp')
        else:
            destFolder = os.path.join(settings.BASE_DIR,'static/assetmgt/temp')
    except Exception as details:
        destFolder = os.path.join(settings.BASE_DIR,'static/assetmgt/temp')        
    tmpfileName = os.path.join(destFolder,"hospital_uploadtemplate.xls")
    #murl = "assetmgt/temp/hospital_uploadtemplate.xls"
    wb.save(tmpfileName)
    #return murl

    response = FileResponse(open(tmpfileName,"rb"))
    #response = HttpResponse(mimetype='application/force-download')
    #response["Accept-Ranges"] = "bytes"
    #response["Content-Length"] = statobj.st_size
    response['Content-Disposition'] = 'attachment; filename=%s'%(os.path.basename(tmpfileName))
    return response


from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse,FileResponse
from assetmgt.models import Hospital,Asset,State,District,AssetMgt,UserProfile
from django.views.generic import View,TemplateView,ListView
from django.views.decorators.csrf import csrf_exempt
#from assetmgt.hospitalforms import HospitalForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
import os
import csv
from django.core.files.storage import FileSystemStorage


DATA_CSV_HEADER = [ "District","Hospital_Name","Hospital_Type(Government/Private)","FullAddress","City","Taluk","PINCODE","Phone_Number(with STD-code)","Total_Doctors","Total_HealthWorkers" ]

class AddHospitalTemplate(LoginRequiredMixin,View):
    '''To render a templet to get hospital Information Invidually '''
    login_url = 'login'
    def get(self,request):
        #hospitalform = HospitalForm()
        #To do user username from request object
        #if not request.user:
        #    print("User----------",request.user.id)
        usr = User.objects.get(username=request.user.username)
        states = State.objects.all()#To do to query the State respect to the user permission
        assets = Asset.objects.all()
        context_dict = {}
        context_dict['states'] = states
        #context_dict['hospitalform'] = hospitalform
        context_dict['assets'] = assets
        return render(request,'assetmgt/add_hospital.html',context=context_dict)


class GetDistrictByState(View):

    def post(self,request):
        stateid = int(request.POST['stateid'])#To do verify stateid mapped in UserProfile also
        districts_dict = {}
        try:
            state = State.objects.get(pk=stateid)
            districts = District.objects.filter(state_id=state)

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
        usr = User.objects.get(username=request.user.username)#To do user username from request object
        states = State.objects.all()#To do to query the State respect to the user permission
        assets = Asset.objects.all()
        states = State.objects.all()
        try:
            #To do get user's distict,state ids 
            stid = int(request.POST['state'])  
            did = int(request.POST['district'])
            tk = request.POST['taluk']
            city = request.POST['city']
            addr = request.POST['haddress']
            pin = request.POST['hpin']
            ht = request.POST['htype']
            nd = int(request.POST['ndoc'])
            nhw = int(request.POST['nhw'])
            hcontact = request.POST['hcontact']
            hname = request.POST['hname']
            #To get State and District Objects
            s = State.objects.get(state_id=stid)
            d = District.objects.get(district_id=did)
            with transaction.atomic():
                hospital_obj = Hospital.objects.create(state_id=s,district_id=d,hospital_name=hname,hospital_type=ht,city=city,taluk=tk,address=addr,contact_number=hcontact,pincode=pin,doctors=nd,healthworkers=nhw)
                asset_name_list = Asset.objects.all().values_list('asset_name',flat=True)
                for asset in asset_name_list:
                    if asset in request.POST:
                        total_asset = int(request.POST[asset])
                        asset_id = Asset.objects.get(asset_name=asset)
                        AssetMgt.objects.create(asset_id=asset_id,hospital_id=hospital_obj,author=usr,asset_total=total_asset)
                        messages.info(request,"Hospital Added successfully")
                    else:
                        print("")
                        continue
            
        except Exception as add_h_err:
            print(add_h_err)
            messages.error(request,"Hospital not added")

        return render(request,'assetmgt/add_hospital.html',{'states':states,'assets':assets})


class GetHospitalSample(View):
    def get(self,request):
        dir_name = settings.MEDIA_ROOT
        extendsion = ".csv"
        sample_file = os.path.join(dir_name,"sample","sample_hospital.csv")
        statobj = os.stat(sample_file)
        usr = UserProfile.objects.get(user__username=request.user.username)
        state_name = usr.state_id.state_name
        district_name = usr.district_id.district_name
        assets_list = Asset.objects.all().values_list('asset_name',flat=True)
        asset_names = list(map(lambda x: "Total_"+x+"_available",assets_list))
        adminstate = usr.adminstate
        global DATA_CSV_HEADER
        if adminstate == 1:
            title_row = DATA_CSV_HEADER[1:]
        elif adminstate == 2:
            title_row = DATA_CSV_HEADER 

        else:
            title_row = list()

        title_row.extend(asset_names)
        print(title_row)
        sample_csv = open(sample_file,"w")
        sample_csv.write(",".join(title_row))
        sample_csv.close()
        response = FileResponse(open(sample_file,"rb"))
        #response = HttpResponse(mimetype='application/force-download')
        response["Accept-Ranges"] = "bytes"
        response["Content-Length"] = statobj.st_size
        response['Content-Disposition'] = 'attachment; filename=%s'%(os.path.basename(sample_file))
        return response
        


class AddMultipleHospital(LoginRequiredMixin,View):
    login_url = 'login'
    def post(self,request):
        states = State.objects.all()
        assets = Asset.objects.all()
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)
            state_obj = usr.state_id
            district_obj = usr.district_id
            myfile = request.FILES['datafile']
            print("---------------------",myfile.name)
            filename = myfile.name
            #Check uploaded file extention is csv
            if not filename.endswith('.csv'):
                messages.error(request,"Only .csv file allowed, Uploaded file is not csv file")
                return render(render,'assetmgt/add_hospital.html',{'states':states,'assets':assets})

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            print("File save in "+str(uploaded_file_url))
            file_path = os.path.join(settings.MEDIA_ROOT,filename)
            print("File path is "+file_path)
            global DATA_CSV_HEADER
            #if os.path.isfile(file_path) and os.path.exists(file_path):i           
            data = csv.DictReader(open(file_path))
            print("Data-----",dir(data))
            for row in data:
                print("Row->",row)
                if usr.adminstate == 2:
                    try:
                        district_obj = District.objects.get(district_name=row[DATA_CSV_HEADER[0]])
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
                                    healthworkers=int(row[DATA_CSV_HEADER[9]])
                                    )
                            asset_name_list = Asset.objects.all().values_list('asset_name',flat=True)
                            for asset in asset_name_list:
                                asset_id = Asset.objects.get(asset_name=asset)
                                try:
                                    total_asset = int(row["Total_"+asset+"_available"])
                                except KeyError as key_not_found:
                                    print("error",key_not_found)
                                    continue
                                AssetMgt.objects.create(asset_id=asset_id,hospital_id=hospital_obj,author=usr.user,asset_total=total_asset)

                            messages.info(request,"Hospital Added successfully")
                    except Exception as er2:
                        print(er2)
                        continue

                else:
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
                                healthworkers=int(row[DATA_CSV_HEADER[9]])
                                )
                        asset_name_list = Asset.objects.all().values_list('asset_name',flat=True)
                        for asset in asset_name_list:
                            asset_id = Asset.objects.get(asset_name=asset)
                            try:
                                total_asset = int(row["Total_"+asset+"_available"])
                            except KeyError as key_not_found:
                                print("error",key_not_found)
                                continue
                            AssetMgt.objects.create(asset_id=asset_id,hospital_id=hospital_obj,author=usr.user,asset_total=total_asset)
                        messages.info(request,"Hospital Added successfully")

        except Exception as er3:
            print("Exception while add multiple hospital ",er3)

        return render(request,'assetmgt/add_hospital.html',{'states':states,'assets':assets})
 

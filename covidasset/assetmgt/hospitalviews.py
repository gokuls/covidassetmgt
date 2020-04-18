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
        #To do user username from request object
        context_dict = {}
        print("User----------",request.user.username)
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)
            states = State.objects.filter(state_name=usr.state_id)#To do to query the State respect to the user permission
            context_dict['usr'] = usr
        except UserProfile.DoesNotExist as usr_profile_not_found:
            print("exception while checking user profile %s"%(usr_profile_not_found))
            states = State.objects.all()#To do to query the State respect to the user permission
        #assets = Asset.objects.all()
        context_dict['states'] = states
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
        assets = Asset.objects.all()

        usr = UserProfile.objects.get(user__username=request.user.username)#To do user username from request object
        try:
            usr = UserProfile.objects.get(user__username=request.user.username)#To do user username from request object
            states = State.objects.filter(state_name=usr.state_id)#To do to query the State respect to the user permission
        except UserProfile.DoesNotExist as e:
            print("exception while add hospital %s"%(str(e)))
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
            opt = int(request.POST['opt'])
            #To get State and District Objects
            s = State.objects.get(state_id=stid)
            d = District.objects.get(district_id=did)
            if opt == 0:
                with transaction.atomic():
                    hospital_obj = Hospital.objects.create(state_id=s,district_id=d,hospital_name=hname,hospital_type=ht,city=city,taluk=tk,address=addr,contact_number=hcontact,pincode=pin,doctors=nd,healthworkers=nhw)
                    messages.info(request,hname+" added successfully") 
                    for asset in assets:
                        AssetMgt.objects.create(asset_id=asset,hospital_id=hospital_obj,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0)
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
                    h.save()
                    messages.info(request,hname+" details updated successfully")
                    print("hospital updated")

        except Exception as add_h_err:
            print("exception in adding single hospital %s"%(str(add_h_err)))
            messages.error(request,hname+" not added")

        return render(request,'assetmgt/add_hospital.html',{'states':states,'usr':usr})


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
        usr = UserProfile.objects.get(user__username=request.user.username)
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
            print("File save in "+str(uploaded_file_url))
            file_path = os.path.join(settings.MEDIA_ROOT,filename)
            print("File path is "+file_path)
            global DATA_CSV_HEADER
            #if os.path.isfile(file_path) and os.path.exists(file_path):i           
            data = csv.DictReader(open(file_path),fieldnames=DATA_CSV_HEADER)
            print("Data-----",dir(data))
            print("number of lines ",data.line_num)
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
                            for asset in assets:
                                AssetMgt.objects.create(asset_id=asset,hospital_id=hospital_obj,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0) 
                            messages.info(request,hospital_obj.hospital_name+" Hospital Added successfully")
                    except District.DoesNotExist as district_nod_found:
                        messages.error(request,"Uploaded file having invalid data "+",".join(row.values()))
                    except ValueError as ver:
                        messages.error(request,"Uploaded file having invalid data for numerical values as \n "+",".join(row.values()))
                    except Exception as er2:
                        print(er2)
                        messages.error(request,"Uploaded file having invalid data "+",".join(row.values()))
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
                        for asset in assets:
                            AssetMgt.objects.create(asset_id=asset,hospital_id=hospital_obj,author=usr.user,asset_total=0,asset_utilized=0,asset_balance=0) 
                        messages.info(request,hospital_obj.hospital_name+" Hospital Added successfully")

        except Exception as er3:
            print("Exception while add multiple hospital ",er3)

        return render(request,'assetmgt/add_hospital.html',{'states':states,'usr':usr})


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
            

class GetReport(View):
    def post(self,request):
        state=hospital=dist=asset=report_option=0
        assetmgt_obj = AssetMgt.objects.all()

        if 'state' in request.POST:
            state = int(request.POST['state'])
            if state:
                assetmgt_obj = AssetMgt.objects.filter(hospital_id__state_id=state)

        if 'dist' in request.POST:
            dist = int(request.POST['district'])
            if dist:
                assetmgt_obj = AssetMgt.objects.filter(hospital_id__district_id=dist)

        if 'opt' in request.POST:
            report_option = request.POST['opt']

        if 'hospital' in request.POST:
            hospital = int(request.POST['hospital'])

        if 'asset' in request.POST:
            asset = int(request.POST['asset'])
        
        if report_option == 1:
            if asset:
                assetmgt_obj = AssetMgt.objects.filter(asset_id=asset)
        elif report_option == 2:
            if hospital:
                assetmgt_obj = AssetMgt.objects.filter(hospital_id=hospital)
        
        userprofile = UserProfile.objects.get(user__username=request.user.username)
        states = State.objects.filter(state_id=userprofile.state_id.state_id)
        districts = District.objects.filter(state_id=userprofile.state_id)
        hospitals = Hospital.objects.filter(state_id=userprofile.state_id,district_id=userprofile.district_id)
        assets = Asset.objects.all()
        context={}
        context['states'] = states
        context['districts'] = districts
        context['hospitals'] = hospitals    
        context['assets'] = assets
        context['user'] = userprofile.user
        context['userprofile'] = userprofile
        context['userstate'] = State.objects.get(state_id=userprofile.state_id_id)
        context['userdistrict'] = District.objects.get(district_id=userprofile.district_id_id)
        context['assetmgts'] = assetmgt_obj


        return render(request,'assetmgt/assetreport.html',{'assets':assetmgt_obj})


class IndexPage(LoginRequiredMixin,View):
    login_url = 'login'
    def get(self,request):
        if request.user.is_authenticated:
            user = request.user.username
        else:
            user = 'not logged in'

        context = {'user':user}
        return render(request,'assetmgt/index-new-1.html',context)



from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse
from assetmgt.models import Hospital,Asset,State,District,AssetMgt
from django.views.generic import View,TemplateView,ListView
from django.views.decorators.csrf import csrf_exempt
#from assetmgt.hospitalforms import HospitalForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages

class AddHospitalTemplate(View):
    '''To render a templet to get hospital Information Invidually '''
    def get(self,request):
        #hospitalform = HospitalForm()
        #To do user username from request object
        #usr = User.objects.get(username='boss')#To do user username from request object
        if not request.user:
            print("User----------",request.user.id)
            usr = User.objects.get(username=request.user.username)
        else:
            usr = User.objects.get(pk=1)   
        states = State.objects.all()#To do to query the State respect to the user permission
        assets = Asset.objects.filter(author=usr)
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
            

class AddHospital(View):
    @transaction.atomic
    def post(self,request):
        #usr = User.objects.get(username='boss')
        #To do user username from request object
        if not request.user:
            usr = User.objects.get(username=request.user.username)#To do user username from request object
        else:
            usr = User.objects.get(id=1)
        #usr = User.objects.get(username='boss')#To do user username from request object
        states = State.objects.all()#To do to query the State respect to the user permission
        assets = Asset.objects.filter(author=usr)
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
            hospital_obj = Hospital.objects.create(state_id=s,district_id=d,hospital_name=hname,hospital_type=ht,city=city,taluk=tk,address=addr,contact_number=hcontact,pincode=pin,doctors=nd,healthworkers=nhw)
            asset_name_list = Asset.objects.all().values_list('asset_name',flat=True)
            for asset in asset_name_list:
                if asset in request.POST:
                    total_asset = int(request.POST[asset])
                    asset_id = Asset.objects.get(asset_name=asset)
                    AssetMgt.objects.create(asset_id=asset_id,hospital_id=hospital_obj,author=usr,asset_total=total_asset)
                else:
                    print("")
                    continue

            messages.info(request,"Hospital Added successfully")
            
        except Exception as add_h_err:
            print(add_h_err)
            messages.error(request,"Hospital not added")

        return render(request,'assetmgt/add_hospital.html',{'states':states,'assets':assets})


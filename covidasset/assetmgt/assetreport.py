from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, JsonResponse

from .models import State
from .models import District
from .models import Hospital
from .models import Asset
from .models import AssetMgt
from .models import UserProfile
from assetmgt import apiviews as apicall

from django.contrib.auth.models import User
from django.views.generic import View,TemplateView,ListView


def assetReport(request):
    context={}
    userprofile = UserProfile.objects.get(user__username=request.user.username)

    if userprofile.adminstate == 0:
        context['message'] = "You are not authorised to access this page"
        return render(request, 'assetmgt/assetreport.html',context=context)

    context['userprofile'] = userprofile
    if request.POST:
        state_id = request.POST['state']
        sel_state = State.objects.get(state_id=state_id).state_name
        try:
            sel_district = District.objects.get(district_id=request.POST['district']).district_name
            district_id = District.objects.get(district_id=request.POST['district']).district_id
        except:
            if request.POST['district'] == "all":
                sel_district = "All District"
                district_id="all"
                
        #sel_opt = request.POST['opt'] if request.POST['opt']!="0" else "Not selected"
        report_by = request.POST['opt']
        context['report_by'] = report_by
        context['reportfor']=" / admin state :  "+sel_state+" / District : "+sel_district+" / Report : "+report_by#context['userstate'].state_name+" userdistrict: "+context['userdistrict'].district_name
    
    assets = Asset.objects.all()
    assetcount = Asset.objects.all().count()
    user = User.objects.get(username=request.user.username)
    states = State.objects.filter(state_id=userprofile.state_id.state_id)
    districts = District.objects.filter(district_id=userprofile.district_id.district_id)
    districts = District.objects.filter(state_id=userprofile.state_id)
    hospitals = Hospital.objects.filter(state_id=userprofile.state_id.state_id,district_id=userprofile.district_id.district_id)
    asset_count = Asset.objects.all().count()

    context['states'] = states
    context['districts'] = districts
    context['hospitals'] = hospitals    
    context['assets'] = assets
    context['user'] = user
    context['userstate'] = State.objects.get(state_id=userprofile.state_id_id)
    context['userdistrict'] = District.objects.get(district_id=userprofile.district_id_id)
    context['assetcount'] = assetcount+1
    if request.POST:
        result_set = generateReport(state_id,district_id,report_by,request)
        if result_set:
            context['assetmgts'] = result_set
            
         
    if 'reportfor' in context:
        context['reportfor']="Report for user : "+user.username+context['reportfor']

    print("context-output:\n",context)
    #context['userhospital'] = Hospital.objetcts.get(hospital_id_id=userprofile.hospital_id_id)
    return render(request, 'assetmgt/assetreport.html',context=context)
 

def generateReport(state_id,district_id,report_by,request):
    assetmgt = None
    if report_by == "by-hospitals":
        if district_id == "all":
            assetmgt = AssetMgt.objects.filter(hospital_id__state_id_id=state_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]
        else:
            assetmgt = AssetMgt.objects.filter(hospital_id__state_id_id=state_id, hospital_id__district_id_id=district_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]        

    if report_by == "by-assets":
            assetmgt = reportByAsset(request,state_id,district_id)        
        

    """if userprofile.adminstate == 1:
        assetmgt = AssetMgt.objects.filter(hospital_id__state_id=userprofile.state_id, hospital_id__district_id=userprofile.district_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]    
    elif userprofile.adminstate == 2:
        assetmgt = AssetMgt.objects.filter(hospital_id__state_id=userprofile.state_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]"""
    #print("------------------------------------------------------------------------\n",assetmgt)
    return assetmgt


def reportByAsset(request,state_id,district_id):

    state_data = list()
    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        #state = user.state_id
        #if "state" in request.GET:
        state = State.objects.get(state_id=state_id)
        districts = District.objects.filter(state_id=user.state_id)
        """if user.adminstate == 1:
            districts = District.objects.filter(state_id=user.state_id.state_id,district_id=user.district_id.district_id)

        if user.adminstate == 0:
            districts = District.objects.filter(state_id=user.state_id.state_id,district_id=user.district_id.district_id)"""
        if district_id == "all":
            districts = District.objects.filter(state_id=state_id)
        else:
            districts = District.objects.filter(state_id=state_id,district_id=district_id)

        assets = Asset.objects.all()#values_list("asset_name",flat=True)
        for district in districts:
            dist_dict = {}
            district_hospitals = Hospital.objects.filter(state_id=state_id,district_id=district.district_id)
                
            if user.adminstate == 0:
                district_hospitals = Hospital.objects.filter(state_id=district.state_id,district_id=district.district_id,hospital_id=user.hospital_id.hospital_id)
            
            h_count = district_hospitals.count()

            dist_dict["district"]=district.district_name
            dist_dict["status"] = {}
            dist_dict["info"]={}
            dist_dict["assets"]={}

            if h_count:
                dist_dict["info"]["healthcentres"]=h_count
                dist_dict["status"]["totalhospitals"] = h_count
                
                for ast in assets:
                    asset_utilized =0
                    asset_total = 0
                    asset_balance = 0
                    try:
                        for hospital in district_hospitals:
                            asset = ast.asset_name.split(" ")
                            asset = "_".join(asset)
                            asset_lower = asset.lower()
                            #assetmgt_object = AssetMgt.objects.filter(hospital_id__district_id=district.district_id,hospital_id=hospital,asset_id__asset_name=asset).annotate(count_asset=Count("hospital_id")).order_by("-creation_date","asset_id","hospital_id")[0].distinct('hospital_id').values('asset_total','asset_utilized','asset_balance')
                            assetmgt_object = AssetMgt.objects.filter(
                                hospital_id__district_id=district.district_id,
                                hospital_id=hospital.hospital_id,asset_id=ast).order_by(
                                "hospital_id","-creation_date").distinct('hospital_id').values(
                                'asset_total','asset_utilized','asset_balance')
                            if assetmgt_object.exists():
                                asset_total = asset_total+assetmgt_object[0]['asset_total']
                                asset_utilized = asset_utilized+assetmgt_object[0]['asset_utilized']
                                asset_balance = asset_balance+assetmgt_object[0]['asset_balance']

                        dist_dict["assets"][asset_lower]={"occupied":asset_utilized,"total":asset_total,"free":asset_balance,"unusable":0}
                        if "bed" in asset_lower:
                            dist_dict["status"]["patientsadmitted"] = asset_utilized
                            dist_dict["status"]["availablebeds"]=asset_balance
                            dist_dict["info"]["patients"] = asset_utilized
                            dist_dict["info"]["freebeds"] = asset_balance

                        if "ventilator" in asset_lower:
                            dist_dict["status"]["availableventilators"]=asset_balance

                    except AssetMgt.DoesNotExist as asset_notfound:
                        print("Exception asset not found in hospital")
                        dist_dict["assets"][asset_lower]={"occupied":0,"total":0,"free":0,"unusable":0}
                        if asset.icontains("bed"):
                            dist_dict["info"]["patients"] = 0
                            dist_dict["info"]["freebeds"] = 0
                        
                        continue
                    except Exception as exp:
                        print("Exception in get state data New  %s"%(str(exp)))
                        continue
            else:
                dist_dict["info"] = { "healthcentres":0,"patients":0,"freebeds":0}
                dist_dict["assets"] = {}
                dist_dict["status"] = { "totalhospitals":0,"patientsadmitted":0,"availablebeds":0,"availableventilators":0}
                for ast in assets:
                    asset_lower = ast.asset_name.split(" ")
                    asset_lower = "_".join(asset_lower)
                    asset_lower = asset_lower.lower()

                    dist_dict["assets"][asset_lower]={"occupied":0,"total":0,"free":0,"unusable":0}

            state_data.append(dist_dict)

    except Exception as er:
        print("Exception while getting data for district %s"%(str(er)))

    #print(state_data)
    return state_data


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


        return render(request,'assetmgt/report_dt.html',{'assets':assetmgt_obj})


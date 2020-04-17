from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse,FileResponse
from assetmgt.models import Hospital,Asset,State,District,AssetMgt,UserProfile
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.db.models import Sum,Count,Min,Max,Avg
from django.core import serializers
import json

def getAllState(request):
    """ To get all state as dictionary """
    states_dict = {}
    states = State.objects.all().values("state_id","state_name")
    if states.exists():
        i = 0
        for state in states:
            states_dict[state["state_id"]]=state["state_name"]
            i += 1
        states_dict["count"]=i

    return JsonResponse({"states":states_dict})



def getTotalCounts(request):
    
    total_counts = dict()
    h_total=0

    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        h_total = Hospital.objects.filter(state_id__state_name=user.state_id).values("hospital_id").count()
        total_counts["totalhospitals"] = h_total
        assets_list = Asset.objects.all().values_list("asset_name",flat=True)
        print(assets_list)
        for asset in assets_list:
            asset_total = AssetMgt.objects.filter(asset_id__asset_name=asset).values("asset_id","hospital_id","asset_total").annotate(hid_count=Count("hospital_id"),latestt_date=Max("creation_date")).aggregate(Sum("asset_total"))
            total_counts["available"+asset+"s"]=asset_total["asset_total__sum"]

        patient_total = AssetMgt.objects.filter(asset_id__asset_name__icontains="bed").values("asset_id","hospital_id","asset_utilized").annotate(hid_count=Count("hospital_id"),latestt_date=Max("creation_date")).aggregate(Sum("asset_utilized"))
        total_counts["patientsadmitted"] = patient_total["asset_utilized__sum"]
    except Exception as ec:
        print(ec)
        total_counts["totalhospitals"]=h_total
        return JsonResponse({"totalcounts":total_counts})

    return JsonResponse(total_counts)

    
        

def getState(request):

    state_data = list()
    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        state = user.state_id
        if "q" in request.GET:
            state = State.objects.get(pk=int(request.GET["q"]))

        districts = District.objects.filter(state_id__state_name=state)
        assets = Asset.objects.all().values_list("asset_name",flat=True)
        for district in districts:
            dist_dict = {}
            h_count = Hospital.objects.filter(state_id=district.state_id,district_id=district.district_id).values("hospital_id").count()
            dist_dict["district"]=district.district_name
            dist_dict["info"]={}
            dist_dict["assets"]={}
            if h_count:
                dist_dict["info"]["healthcentres"]=h_count
                for asset in assets:
                    try:
                        assetmgt_object = AssetMgt.objects.filter(hospital_id__district_id=district.district_id,asset_id__asset_name=asset).annotate(count_asset=Count("hospital_id")).order_by("-creation_date","asset_id").aggregate(Sum("asset_utilized"),Sum("asset_balance"),Sum("asset_total"))
                        dist_dict["assets"][asset+"s"]={"occupied":assetmgt_object["asset_utilized__sum"],"total":assetmgt_object["asset_total__sum"],"free":assetmgt_object["asset_balance__sum"],"unusable":0}
                        if "bed" in asset:
                            dist_dict["info"]["patients"] = assetmgt_object["asset_utilized__sum"]
                            dist_dict["info"]["freebeds"] = assetmgt_object["asset_balance__sum"]

                    except AssetMgt.DoesNotExist as asset_notfound:
                        print("Exception asset not found in hospital")
                        dist_dict["assets"][asset+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}
                        if asset.icontains("bed"):
                            dist_dict["info"]["patients"] = 0
                            dist_dict["info"]["freebeds"] = 0
                        
                        continue
            else:
                dist_dict["info"] = { "healthcentres":0,"patients":0,"freebeds":0}
                dist_dict["assets"] = {}
                for asset in assets:
                    dist_dict["assets"][asset+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}

            state_data.append(dist_dict)

    except Exception as er:
        print("Exception while getting data for district %s is %s"%(district.district_name,str(er)))

    print(state_data)
    return JsonResponse({"state":state_data})



def getHospitalsByDistrict(request):

    try:
        district=request.GET['q']
        district_data = list()
        asset_dict = {}
        districtobj=District.objects.get(district_name=district)
        #dis_hospitals = Hospital.objects.get(district_id_id=districtobj)
        serialized_data = serializers.serialize('json', Hospital.objects.filter(district_id_id=districtobj),
                use_natural_foreign_keys=True, fields=['hospital_name', 'latitude', 'longitude','hospital_id'], indent=4)
        
        #print(serialized_data)
        assets = Asset.objects.all()
        for ast in assets:
            asset_dict[ast.asset_id]=ast.asset_name
            
        print("Assets",asset_dict)
        #aasetmgt_serialized_data = serializers.serialize('json', AssetMgt.objects.filter(hospital_id__district_id=1).select_related('hospital_id').order_by('hospital_id','asset_id','creation_date'),use_natural_foreign_keys=True, fields=['asset_id','hospital_id','asset_utilized','asset_total','asset_balance'], indent=4)
        aasetmgt_serialized_data = serializers.serialize('json', AssetMgt.objects.filter(hospital_id__district_id=districtobj).order_by('hospital_id','asset_id','-creation_date').distinct('hospital_id','asset_id'),use_natural_foreign_keys=True, fields=['asset_id', 'hospital_id','asset_utilized','asset_total','asset_balance'], indent=4)
        
        #print(aasetmgt_serialized_data)
        hospital_data = json.loads(serialized_data)
        asset_mgt_data = json.loads(aasetmgt_serialized_data)
        for h_data in hospital_data:
            hospital_dict = {}
            hospital_dict['name']=h_data['fields']['hospital_name']
            hospital_dict["location"] = (h_data["fields"]["latitude"],h_data["fields"]["longitude"])
            hospital_dict["assets"] = {}
            for asset in asset_mgt_data:
                if h_data['pk']==asset['fields']['hospital_id']:
                    print(asset['fields']['asset_id'],h_data['pk'])
                    asset_obj = Asset.objects.get(asset_id=asset['fields']['asset_id'])
                    hospital_dict["assets"][asset_obj.asset_name] = {"occupied":asset["fields"]["asset_utilized"],"free":asset["fields"]["asset_balance"],"unusable":0}
                    if "bed" in asset_obj.asset_name.lower():
                        hospital_dict["patients"] = asset["fields"]["asset_utilized"]
            district_data.append(hospital_dict)

    except Exception as ed:
        print(ed)

    print(district_data)

    return JsonResponse({district:district_data}) 


 



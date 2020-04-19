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

    #return JsonResponse({"states":states_dict})
    return JsonResponse(states_dict)


def getStateNameById(request):
    state_id = request.GET['q']
    state_name = None
    try:
        state_id = int(state_id)
        state_name = State.objects.get(pk=request.user.userprofile.state_id.state_id).state_name
    except State.DoesNotExist as state_not_found:
        print("Exception state name not found for given state id",state_id)

    return JsonResponse({"stateName":state_name})   

def getTotalCounts(request):
    
    total_counts = dict()
    h_total=0

    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        #state = request.GET['state']
        print("users admin state",user.adminstate)
        h_total = 0
        state_hospitals = Hospital.objects.filter(state_id__state_name=user.state_id)
        if user.adminstate == 1:
            state_hospitals = Hospital.objects.filter(district_id=user.district_id)
            #h_total = Hospital.objects.filter(district_id=user.district_id).count()
            h_total = state_hospitals.count()
        elif user.adminstate == 0:
            state_hospitals = Hospital.objects.filter(state_id__state_name=user.state_id,district_id__district_name=user.district_id,hospital_id=user.hospital_id.hospital_id)
            #h_total = state_hospitals.values('hospital_id').count()
            h_total = state_hospitals.count()
        else:
            state_hospitals = Hospital.objects.filter(state_id=user.state_id)
            h_total = state_hospitals.count()
            #h_total = Hospital.objects.filter(state_id=user.state_id).count()
            #h_toatal = state_hospitals.values('hospital_id').count()

        #state_hospitals = Hospital.objects.filter(state_id__state_name=state)
        #h_toatal = state_hospitals.values('hospital_id').count()
        print("Total hospital under user %s is %d"%(user,h_total))
        total_counts["totalhospitals"] = h_total
        assets_list = Asset.objects.all().values_list("asset_name",flat=True)
        print(assets_list)
        asset_total=asset_utilized=asset_balance=0
        for asset in assets_list:
            asset_lower = asset.lower()
            for hospital in state_hospitals:
                try:
                    assetmgt_obj = AssetMgt.objects.filter(asset_id__asset_name=asset,hospital_id=hospital,hospital_id__state_id__state_name=user.state_id).order_by('hospital_id','-creation_date').distinct('hospital_id').values('asset_total','asset_utilized','asset_balance')
                    if assetmgt_obj.exists():
                        asset_total += assetmgt_obj[0]['asset_total']
                        asset_utilized += assetmgt_obj[0]['asset_utilized']
                        asset_balance += assetmgt_obj[0]['asset_balance']

                except AssetMgt.DoesNotExist as asset_not_found:
                    print("exception while getting asset_toatl for state is %s"%(str(asset_notfound)))
                    continue
            total_counts["available"+asset_lower+"s"] = asset_balance 
            if 'bed' in asset_lower:
                total_counts['patientsadmitted'] = asset_utilized

    except Exception as ec:
        print(ec)
        total_counts["totalhospitals"]=h_total
        return JsonResponse({"totalcounts":total_counts})

    return JsonResponse(total_counts)

    
        

def getStateAllDateCumulative(request):

    state_data = list()
    try:
        #user = UserProfile.objects.get(user__username=request.user.username)
        #state = user.state_id
        if "q" in request.GET:
            state = State.objects.get(state_id=int(request.GET["q"]))

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
                        assetmgt_object = AssetMgt.objects.filter(hospital_id__district_id=district.district_id,asset_id__asset_name=asset).annotate(count_asset=Count("hospital_id")).order_by("-creation_date","asset_id","hospital_id").aggregate(Sum("asset_utilized"),Sum("asset_balance"),Sum("asset_total"))
                        dist_dict["assets"][asset.lower()+"s"]={"occupied":assetmgt_object["asset_utilized__sum"],"total":assetmgt_object["asset_total__sum"],"free":assetmgt_object["asset_balance__sum"],"unusable":0}
                        if "bed" in asset.lower():
                            dist_dict["info"]["patients"] = assetmgt_object["asset_utilized__sum"]
                            dist_dict["info"]["freebeds"] = assetmgt_object["asset_balance__sum"]

                    except AssetMgt.DoesNotExist as asset_notfound:
                        print("Exception asset not found in hospital")
                        dist_dict["assets"][asset.lower()+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}
                        if asset.icontains("bed"):
                            dist_dict["info"]["patients"] = 0
                            dist_dict["info"]["freebeds"] = 0
                        
                        continue
            else:
                dist_dict["info"] = { "healthcentres":0,"patients":0,"freebeds":0}
                dist_dict["assets"] = {}
                for asset in assets:
                    dist_dict["assets"][asset.lower()+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}

            state_data.append(dist_dict)

    except Exception as er:
        print("Exception while getting data for district %s"%(str(er)))

    print(state_data)
    return JsonResponse(state_data,safe=False)



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
            hospital_dict["location"] = [h_data["fields"]["latitude"],h_data["fields"]["longitude"]]
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

    return JsonResponse(district_data,safe=False) 


 

def getStateNew(request):

    state_data = list()
    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        #state = user.state_id
        #if "state" in request.GET:
        state = State.objects.get(state_name=request.GET["state"])

        #districts = District.objects.filter(state_id=state)
        districts = District.objects.filter(state_id=user.state_id.state_id)
        assets = Asset.objects.all().values_list("asset_name",flat=True)
        for district in districts:
            dist_dict = {}
            h_count = Hospital.objects.filter(state_id=district.state_id,district_id=district.district_id).values("hospital_id").count()
            district_hospitals = Hospital.objects.filter(state_id=district.state_id,district_id=district.district_id)

            dist_dict["district"]=district.district_name
            dist_dict["info"]={}
            dist_dict["assets"]={}

            if h_count:
                dist_dict["info"]["healthcentres"]=h_count
                asset_utilized=asset_total=asset_balance = 0
                for asset in assets:
                    try:
                        for hospital in district_hospitals:
                            asset_lower = asset.lower()
                            #assetmgt_object = AssetMgt.objects.filter(hospital_id__district_id=district.district_id,hospital_id=hospital,asset_id__asset_name=asset).annotate(count_asset=Count("hospital_id")).order_by("-creation_date","asset_id","hospital_id")[0].distinct('hospital_id').values('asset_total','asset_utilized','asset_balance')
                            assetmgt_object = AssetMgt.objects.filter(hospital_id__district_id=district.district_id,hospital_id=hospital,asset_id__asset_name=asset).order_by("hospital_id","-creation_date").distinct('hospital_id').values('asset_total','asset_utilized','asset_balance')
                            if assetmgt_object.exists():
                                asset_total += assetmgt_object[0]['asset_total']
                                asset_utilized += assetmgt_object[0]['asset_utilized']
                                asset_balance += assetmgt_object[0]['asset_balance']

                        dist_dict["assets"][asset_lower+"s"]={"occupied":asset_utilized,"total":asset_total,"free":asset_balance,"unusable":0}
                        if "bed" in asset_lower:
                            dist_dict["info"]["patients"] = asset_utilized
                            dist_dict["info"]["freebeds"] = asset_balance

                    except AssetMgt.DoesNotExist as asset_notfound:
                        print("Exception asset not found in hospital")
                        dist_dict["assets"][asset_lower+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}
                        if asset.icontains("bed"):
                            dist_dict["info"]["patients"] = 0
                            dist_dict["info"]["freebeds"] = 0
                        
                        continue
            else:
                dist_dict["info"] = { "healthcentres":0,"patients":0,"freebeds":0}
                dist_dict["assets"] = {}
                for asset in assets:
                    asset_lower = asset.lower()
                    dist_dict["assets"][asset_lower+"s"]={"occupied":0,"total":0,"free":0,"unusable":0}

            state_data.append(dist_dict)

    except Exception as er:
        print("Exception while getting data for district %s"%(str(er)))

    print(state_data)
    return JsonResponse(state_data,safe=False)

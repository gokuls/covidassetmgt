from django.shortcuts import render
#from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse

from .models import State
from .models import District
from .models import Hospital, HospitalType
from .models import Asset
from .models import AssetMgt
from .models import UserProfile



'''def get_all_states():
    states=State.objects.all()
    print(states)'''
    
@csrf_exempt  
def get_all_states(request):#getAllState():
    """ To get all state as dictionary """
    states_dict = {}
    states = State.objects.all().values("state_id","state_name")
    if states.exists():
        i = 0
        for state in states:
            states_dict[state["state_id"]]=state["state_name"]
            i += 1
        #states_dict["count"]=i
    print(states_dict)
    #return JsonResponse({"states":states_dict})
    return JsonResponse(states_dict)
    #return HttpResponse(states_dict)
    #return HttpResponse(json.dumps(states_dict), content_type='application/json')

def get_all_districts_by_state(request):#getAllState():
    """ To get all state as dictionary """
    stateid = request.GET['stateid']
    dists_dict = {}
    districts = District.objects.filter(state_id=stateid).values("district_id","district_name")
    if districts.exists():
        i = 0
        for district in districts:
            dists_dict[district["district_id"]]=district["district_name"]
            i += 1
        #dists_dict["count"]=i
    print(dists_dict)
    #return JsonResponse({"states":states_dict})
    return JsonResponse(dists_dict)
    #return HttpResponse(dists_dict)

def get_all_assets(request):#getAllState():
    """ To get all state as dictionary """
    state_id = request.GET['stateid']
    district_id = request.GET['districtid']
    assets_dict = {}
    assets = Asset.objects.all().values("asset_id","asset_name")
    if assets.exists():
        i = 0
        for asset in assets:
            assets_dict[asset["asset_id"]]=asset["asset_name"]
            i += 1
        #states_dict["count"]=i
    print(assets_dict)
    #return JsonResponse({"states":states_dict})
    return JsonResponse(assets_dict)
    #return HttpResponse(assets_dict)
    
def get_hospitals_with_assets(request):
    state_id = request.GET['stateid']
    district_id = request.GET['districtid']
    asset_id = request.GET['assetid']
    
    data_table_list = []
    h_assets = AssetMgt.objects.filter(hospital_id__state_id_id=state_id, hospital_id__district_id_id=district_id,asset_id=asset_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")
    
    if h_assets.exists():
        i=0
        for h_asset in h_assets:
            data_table={}
            data_table['hname']=h_asset.hospital_id.hospital_name
            data_table['aname']=h_asset.asset_id.asset_name
            data_table['atot']=h_asset.asset_total
            data_table['autil']=h_asset.asset_utilized
            data_table['abal']=h_asset.asset_balance
            data_table_list.append(data_table)
            i += 1
    print(data_table_list)
    return JsonResponse(data_table_list,safe=False)   
    #return JsonResponse(json.dumps(data_table_list), content_type='application/json')         
                
    

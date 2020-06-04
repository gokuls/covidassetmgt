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
    dists_dict = {}
    districts = District.objects.filter(state_id=1).values("district_id","district_name")
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
    

    

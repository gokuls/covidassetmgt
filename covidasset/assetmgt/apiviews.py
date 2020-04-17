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


def getAllState(request):
    ''' To get all state as dictionary '''
    states_dict = {}
    states = State.objects.all().values('state_id','state_name')
    if states.exists():
        i = 0
        for state in states:
            states_dict[state['state_id']]=state['state_name']
            i += 1
        states_dict['count']=i

    return JsonResponse({'states':states_dict})



def getTotalCounts(request):
    
    total_counts = dict()
    h_total=0

    try:
        user = UserProfile.objects.get(user__username=request.user.username)
        h_total = Hospital.objects.filter(state_id__state_name=user.state_id).values('hospital_id').count()
        total_counts["totalhospitals"] = h_total
        assets_list = Asset.objects.all().values_list('asset_name',flat=True)
        print(assets_list)
        for asset in assets_list:
            asset_total = AssetMgt.objects.filter(asset_id__asset_name=asset).values('asset_id','hospital_id','asset_total').annotate(hid_count=Count('hospital_id'),latestt_date=Max('creation_date')).aggregate(Sum('asset_total'))
            total_counts["available"+asset+"s"]=asset_total['asset_total__sum']

        patient_total = AssetMgt.objects.filter(asset_id__asset_name__icontains='bed').values('asset_id','hospital_id','asset_utilized').annotate(hid_count=Count('hospital_id'),latestt_date=Max('creation_date')).aggregate(Sum('asset_utilized'))
        total_counts["patientsadmitted"] = patient_total['asset_utilized__sum']
    except Exception as ec:
        print(ec)
        total_counts['totalhospitals']=h_total
        return JsonResponse({'totalcounts':total_counts})

    return JsonResponse(total_counts)

    
        


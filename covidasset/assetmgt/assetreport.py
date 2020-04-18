from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse 

from .models import State
from .models import District
from .models import Hospital
from .models import Asset
from .models import AssetMgt
from .models import UserProfile
from django.contrib.auth.models import User


def assetReport(request):
    """states = State.objects.all()
    districts = District.objects.all()
    hospitals = Hospital.objects.all()
    assets = Asset.objects.all()
    user = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user__username=request.user.username)
    assetmgt = AssetMgt.objects.filter(hospital_id__state_id=userprofile.state_id)
    context={}
    context['states'] = states
    context['districts'] = districts
    context['hospitals'] = hospitals    
    context['assets'] = assets
    context['user'] = user
    context['userprofile'] = userprofile
    context['userstate'] = State.objects.get(state_id=userprofile.state_id_id)
    context['userdistrict'] = District.objects.get(district_id=userprofile.district_id_id)"""
    userprofile = UserProfile.objects.get(user__username=request.user.username)
    if userprofile.adminstate == 0:
        print("hello")
        context['message'] = "You are not authorised to access this page"
        return render(request, 'assetmgt/assetreport.html',context=context)

    assets = Asset.objects.all()
    user = User.objects.get(username=request.user.username)
    states = State.objects.filter(state_id=userprofile.state_id.state_id)
    districts = District.objects.filter(district_id=userprofile.district_id.district_id)
    hospitals = Hospital.objects.filter(state_id=userprofile.state_id.state_id,district_id=userprofile.district_id.district_id)
    asset_count = Asset.objects.all().count()
    context={}
    if userprofile.adminstate == 1:
        assetmgt = AssetMgt.objects.filter(hospital_id__state_id=userprofile.state_id, hospital_id__district_id=userprofile.district_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]    
    elif userprofile.adminstate == 2:
        assetmgt = AssetMgt.objects.filter(hospital_id__state_id=userprofile.state_id).order_by("hospital_id","asset_id","-creation_date").distinct("hospital_id","asset_id")#[:asset_count]

    context['states'] = states
    context['districts'] = districts
    context['hospitals'] = hospitals    
    context['assets'] = assets
    context['user'] = user
    context['userprofile'] = userprofile
    context['userstate'] = State.objects.get(state_id=userprofile.state_id_id)
    context['userdistrict'] = District.objects.get(district_id=userprofile.district_id_id)
    context['assetmgts'] = assetmgt
    #context['userhospital'] = Hospital.objetcts.get(hospital_id_id=userprofile.hospital_id_id)
    return render(request, 'assetmgt/assetreport.html',context=context)

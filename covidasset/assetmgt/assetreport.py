from django.shortcuts import render
from django.http import Http404

from .models import State
from .models import District
from .models import Hospital
from .models import Asset
from .models import AssetMgt


def assetReport(request):
    states = State.objects.all()
    districts = District.objects.all()
    hospitals = Hospital.objects.all()
    assets = Asset.objects.all()
    user = User.objects.get(username=request.user.username)
    context={}
    context['states'] = states
    context['districts'] = districts
    context['hospitals'] = hospitals    
    context['assets'] = assets
    context['user'] = user
    return render(request, 'assetmgt/assetreport.html')

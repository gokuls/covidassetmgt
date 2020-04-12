from django.shortcuts import render
from django.http import Http404


from .models import Asset
# Create your views here.

def Asset(request):
    """ Asset Master Details"""

    try:
        asset_val = Asset.objects.all()
    except Asset.DoesNotExist:
        raise Http404('No Data Found')
    return render(request,'assetmgt/asset.html',{'asset':asset_val})

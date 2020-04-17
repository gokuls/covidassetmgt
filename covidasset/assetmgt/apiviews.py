from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse,FileResponse
from assetmgt.models import Hospital,Asset,State,District,AssetMgt,UserProfile
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
#from assetmgt.hospitalforms import HospitalForm
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from django.conf import settings
import os
import csv
from django.core.files.storage import FileSystemStorage


def getAllState(request):
    ''' To get all state as dictionary '''
    states_dict = {}
    states = State.objects.all().values('state_id','state_name')
    if states.exists():
        i = 0
        for state in states:
            states_dict[state.state_id]=state.state_name
            i += 1
        states_dict['count']=i

    return JsonResponse({'states':states_dict})




        


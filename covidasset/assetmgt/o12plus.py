from django.shortcuts import render
from django.http import Http404


from .models import Asset
from .models import State
from .models import District
from .models import Hospital
from .models import ( AssetMgt ,
                    HospitalType  ,
                    HtypeAssetMapping,
                    HospAssetMapping  )

from .models import AssetMgt


from .views import xlsGenerate

from django.contrib import messages

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse 

from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.auth import logout
from django.forms import formset_factory

from django.db import DatabaseError, transaction

import json
from django.views.generic.edit import CreateView
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url

import xlwt
import time



from math import cos,sin,sqrt,asin,floor,radians
import os
import csv


STATECODE = {'AN':'Andaman and Nicobar Islands',
'AP':'Andhra Pradesh',
'AR':'Arunachal Pradesh',
'AS':'Assam',
'BR':'Bihar',
'CH':'Chandigarh',
'CT':'Chhattisgarh',
'DD':'Daman and Diu',
'DL':'Delhi',
'DN':'Dadra and Nagar Haveli',
'GA':'Goa',
'GJ':'Gujarat',
'HP':'Himachal Pradesh',
'HR':'Haryana',
'JH':'Jharkhand',
'JK':'Jammu and Kashmir',
'KA':'Karnataka',
'KL':'Kerala',
'LD':'Lakshadweep',
'MH':'Maharashtra',
'ML':'Meghalaya',
'MN':'Manipur',
'MP':'Madhya Pradesh',
'MZ':'Mizoram',
'NL':'Nagaland',
'OR':'Odisha',
'PB':'Punjab',
'PY':'Puducherry',
'RJ':'Rajasthan',
'SK':'Sikkim',
'TG':'Telangana',
'TN':'TamilNadu',
'TR':'Tripura',
'UP':'Uttar Pradesh',
'UT':'Uttarakhand',
'WB':'West Bengal'}

proximity = 20
def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371
    
    return c * r



def returnHospitals(request):
	try:
		## Write code to get state id.

		#get the list of hospitals with latitude and longitude

		ulat = float(request.GET['current_lat'])
		ulon = float(request.GET['current_lon'])
		dist = int(request.GET['limit'])
		statecode = request.GET['state_code']

		#stateid = 1
		stateobj = State.objects.get(state_name=STATECODE[statecode])
		hospitallist = Hospital.objects.filter(state_id=stateobj)

		shortlist = []

		for i in hospitallist:
			if i.latitude:
				d = haversine(ulat,ulon,float(i.latitude),float(i.longitude))
				print(d)
				if d <= dist:
					shortlist.append(i)

		ast = []
		ast.append(Asset.objects.get(asset_name='Bed'))
		ast.append(Asset.objects.get(asset_name='ventilator'))
		ast.append(Asset.objects.get(asset_name='Oxygen-cylinder'))

		dt = []
		for i in shortlist:
			tempd = dict()
			tempd['name'] = i.hospital_name
			tempd['latitude'] = i.latitude
			tempd['longitude'] = i.longitude

			tempd['assets'] = dict()
			for assetobj in ast:
				asto = AssetMgt.objects.filter(
					hospital_id=i,asset_id=assetobj).last()
				if asto:
					tempd['assets'][assetobj.asset_name] = dict()
					tempd['assets'][assetobj.asset_name]['occupied'] = asto.asset_utilized
					tempd['assets'][assetobj.asset_name]['free'] = asto.asset_balance
					tempd['assets'][assetobj.asset_name]['unusable'] = 0
			dt.append(tempd)


		print(shortlist)
		rdata = {}
		rdata['status'] = True
		rdata['data'] = dt
		return JsonResponse(rdata,safe=False)

	except Exception as details: 
		print(details)
		rdata = {}
		rdata['status'] =  False
		return JsonResponse(rdata)
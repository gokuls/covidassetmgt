from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse,JsonResponse
from assetmgt.models import Hospital,Asset,State,District
from django.views.generic import View,TemplateView,ListView
from django.views.decorators.csrf import csrf_exempt
from assetmgt.hospitalforms import HospitalForm
from django.contrib.auth.models import User

class AddHospitalTemplate(View):
    '''To render a templet to get hospital Information Invidually '''
    def get(self,request):
        hospitalform = HospitalForm()
        usr = User.objects.get(username='karthikeyant')#To do user username from request object
        states = State.objects.all()#To do to query the State respect to the user permission
        assets = Asset.objects.filter(author=usr)
        context_dict = {}
        context_dict['states'] = states
        context_dict['hospitalform'] = hospitalform
        context_dict['assets'] = assets
        return render(request,'assetmgt/add_hospital.html',context=context_dict)


class GetDistrictByState(View):

    def post(self,request):
        stateid = int(request.POST['stateid'])#To do verify stateid mapped in UserProfile also
        districts_dict = {}
        try:
            state = State.objects.get(pk=stateid)
            districts = District.objects.filter(state_id=state)

        except State.DoesNotExist as state_not_found:
            print(state_not_found)
            
        return render(request,"assetmgt/district_dropdown_list.html",{'dist':districts})
            

class AddHospital(View):
    def post(self,request):

        stid = int(request.POST['state'])
        did = int(request.POST['district'])
        tk = request.POST['taluk']
        city = requet.POST['city']
        addr = request.POST['address']
        pin = request.POST['pin']
        ht = request.POST['htype']
        nd = int(request.POST['ndoc'])
        nhw = int(request.POST['nhw'])
        hcontact = requet.POST['hcontact']



        return render(request,'assetmgt/add_hospital.html',{})


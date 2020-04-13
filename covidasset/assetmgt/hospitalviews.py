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
            districts = District.objects.filter(state_id=state).values('district_id','district_name')
            if districts:
                for district in districts:
                    districts_dict[district.district_id] = district.district_name

        except State.DoesNotExist as state_not_found:
            print(state_not_found)
            
        return JsonResponse({'data':districts_dict})
            




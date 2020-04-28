from django.shortcuts import render
from django.http import Http404


from .models import Asset
from .models import State
from .models import District
from .models import Hospital

from .forms import ExtendedUserCreationForm
from .forms import UserProfileForm
from .forms import HospitalForm

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate 
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def index(request):
	if request.user.is_authenticated:
		user = request.user.username
	else:
		user = 'not logged in'

	context = {'user':user}
	return render(request,'assetmgt/fomndtable.html',context)


@login_required
def register(request):
	if request.user.userprofile.adminstate < 2:
		messages.info(request,"You are not Authorised to View this page ")
		return redirect('index')
	if request.method == 'POST':
		form = ExtendedUserCreationForm(request.POST)
		profile_form = UserProfileForm(request.POST)


		if form.is_valid() and profile_form.is_valid():
			

			print("form is valid")
			profile = profile_form.save(commit=False)
			if not profile.adminstate:
				print(profile.hospital_id)
				if not profile.hospital_id:
					messages.info(request,"Select The Hospital for Hospital Admin")
					context = {'form' : form, 'profile_form':profile_form} 
					return render(request,'assetmgt/adduser.html',context)

			user = form.save()

			profile.user = user 

			profile.save()

			username = form.cleaned_data.get('username')
			#password = form.cleaned_data.get('password1')

			
			messages.info(request,"User %s Addded Sucessfully"%username)
            #url = reverse('assetmanagementview')

            #return HttpResponseRedirect(url)

			return redirect('register')
		else:
			print(profile_form.errors)
	else:
		form = ExtendedUserCreationForm()
		try:
			state = State.objects.get(state_id=request.user.userprofile.state_id.state_id)
			profile_form = UserProfileForm(initial={'stateid':state})
		except Exception as details:
			print(details)
			profile_form = UserProfileForm()
 
	context = {'form' : form,
			'profile_form':profile_form}
	return render(request,'assetmgt/adduser.html',context)



def addHospital(request):
	if request.method == 'POST':
		form = HospitalForm(request.POST)


		if form.is_valid():
			user = form.save()
			return redirect('index')

	else:
		form = HospitalForm()
		
	context = {'form' : form,
			}
	return render(request,'assetmgt/addhospital.html',context)


def load_district(request):
    state_id = request.GET.get('state')
    state = State.objects.get(state_id=state_id)
    dist = District.objects.filter(state_id=state).order_by('district_name')
    return render(request, 'assetmgt/district_dropdown_list.html', {'dist': dist})

def load_hospital(request):
    distid = request.GET.get('distid')
    dist = District.objects.get(district_id=distid)
    hospitals = Hospital.objects.filter(district_id=dist).order_by('hospital_name')
    return render(request, 'assetmgt/hospital_dropdown_list.html', {'hospitals': hospitals})




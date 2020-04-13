from django.shortcuts import render
from django.http import Http404


from .models import Asset
from .models import State
from .models import District

from .forms import ExtendedUserCreationForm
from .forms import UserProfileForm

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import authenticate 
from django.contrib.auth import login


def index(request):
	if request.user.is_authenticated:
		user = request.user.username
	else:
		user = 'not logged in'

	context = {'user':user}
	return render(request,'assetmgt/index.html',context)


def register(request):
	if request.method == 'POST':
		form = ExtendedUserCreationForm(request.POST)
		profile_form = UserProfileForm(request.POST)


		if form.is_valid() and profile_form.is_valid():
			user = form.save()

			print("form is valid")
			profile = profile_form.save(commit=False)
			profile.user = user 

			profile.save()

			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')

			user = authenticate(username = username,
					password=password)
			login(request,user)

			return redirect('index')
		else:
			print(profile_form.errors)
	else:
		form = ExtendedUserCreationForm()
		profile_form = UserProfileForm()
 
	context = {'form' : form,
			'profile_form':profile_form}
	return render(request,'assetmgt/adduser.html',context)

def load_district(request):
    state_id = request.GET.get('state')
    state = State.objects.get(state_id=state_id)
    dist = District.objects.filter(state_id=state).order_by('district_name')
    return render(request, 'assetmgt/district_dropdown_list.html', {'dist': dist})
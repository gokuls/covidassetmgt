from django.shortcuts import render
from django.http import Http404


from .models import Asset
from .models import State
from .models import District
from .models import Hospital

from .forms import ExtendedUserCreationForm
from .forms import UserProfileForm
from .forms import HospitalForm
from .forms import AssetForm

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse 
from django.http import  HttpResponseRedirect
from django.contrib.auth import authenticate 
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LoginForm
from django.db import IntegrityError


def LoginMeth(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':

        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
           username =  form.cleaned_data['username']
           password = form.cleaned_data['password']

           user = authenticate(username=username, password=password)
           if user is not None:
               if user.is_active:
                   login(request, user)
                   #alogger.info("%s user logged in from %s"%(username,request.META['REMOTE_ADDR']))
                   url = reverse('index')
                   return HttpResponseRedirect(url)

               else:
                   context_dict = { 'status' : "incorrect credentials" }
                   return render(request,'assetmgt/login.html',context=context_dict)
           else:
               context_dict = { 'status' : "Login failure" }
               form = LoginForm()
               return render(request, 'assetmgt/login.html', {'form': form,'error':True})
    else:
        form = LoginForm()
    return render(request, 'assetmgt/login.html', {'form': form})

def AssetsView(request):
	'''
		Page to view the asset and add the Asset 
	'''
	assets = Asset.objects.all()
	context = dict()

	context['assets'] = assets

	return render(request,
				 'assetmgt/assetview.html',
				 context)


def returnAssetForm(request):
    """
    Method returns Service Form
    """
    inidict = {}
    inidict['author'] = request.user
    form = AssetForm(initial=inidict)

    return render(request, 'snippets/pform.html', {
                  'form':form
                  })


@login_required
def addAsset(request):
    if request.method == 'POST':
        try:
            form = AssetForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.author = request.user
                obj.save()
                #messages.info(request,'Asset Added')
                return HttpResponse("Done")
            else:
                return HttpResponse("Error")
        except IntegrityError as ie:
            print("Asset already exists")
            return HttpReposnse("AE")

        except Exception as details:
            print("adding policy "+details)
            return HttpResponse("Error")
    return HttpResponse("Done")

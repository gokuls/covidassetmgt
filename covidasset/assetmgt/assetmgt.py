from django.shortcuts import render
from django.http import Http404


from .models import Asset
from .models import State
from .models import District
from .models import Hospital
from .models import AssetMgt

from .forms import ExtendedUserCreationForm
from .forms import UserProfileForm
from .forms import HospitalForm
from .forms import AssetForm
from .forms import AssetMgtForm

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

from django.template.loader import render_to_string
from django.contrib.auth import logout


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


def returnAssetMgtForm(request):
    """
    Method returns Service Form
    """
    if request.method == 'POST':
        if 'hospital_id' in request.POST:
            hid = request.POST['hospital_id']
            try:
                inidict = {}
                inidict['hospital_id'] = Hospital.objects.get(hospital_id=hid)
                form = AssetMgtForm(initial=inidict)
                return render(request, 'snippets/pform.html', {
                  'form':form
                  })
            except Exception as details:
                print(details)
                return HttpResponse("Select Hospital")
        else:
            return HttpResponse("Select Hospital")
    else:
        return HttpResponse("Select Hospital")

    



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
            return HttpResponse("AE")

        except Exception as details:
            print("adding policy "+details)
            return HttpResponse("Error")
    return HttpResponse("Done")



@login_required
def addAssetManagement(request):
    if request.method == 'POST':
        try:
            form = AssetMgtForm(request.POST)
            if form.is_valid():
                print("Form is valid")
                obj = form.save(commit=False)

                obj.author = request.user
                obj.asset_balance = obj.asset_total - obj.asset_utilized
                obj.save()
                #messages.info(request,'Asset Added')
                return HttpResponse("Done")
            else:
                return HttpResponse("Error")
        except IntegrityError as ie:
            print("Asset already exists")
            return HttpResponse("AE")

        except Exception as details:
            print("adding policy "+details)
            return HttpResponse("Error")
    return HttpResponse("Done")


def AssetManagementView(request):
    if request.user:
        user = request.user 
        if user.userprofile.adminstate == 0:
            print('Hospital admin')
            hosp = Hospital.objects.get(hospital_id=user.userprofile.hospital_id.hospital_id)
            rendered = render_to_string('assetmgt/hospitaladmin.html', {'hospitals': hosp})

            assetmt = AssetMgt.objects.filter(hospital_id=user.userprofile.hospital_id.hospital_id)
        elif user.userprofile.adminstate == 1:
            print("District admin")
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
            rendered = render_to_string('assetmgt/districtadmin.html', {'hospitals': hosp })
            hids = Hospital.objects.filter(
                        district_id=user.userprofile.district_id.district_id
                        ).values_list('hospital_id',flat=True)
            assetmt = AssetMgt.objects.filter(hospital_id__in=hids)
        else:
            print("State Admin ")
            dist = District.objects.filter(state_id=user.userprofile.state_id.state_id)
            hids = Hospital.objects.filter(
                        state_id=user.userprofile.state_id.state_id
                        ).values_list('hospital_id',flat=True)
            rendered = render_to_string('assetmgt/stateadmin.html', {'dist': dist})
            assetmt = AssetMgt.objects.all()
        context = dict()
        

        context['selecthospital'] = rendered
        context['assetmgt'] = assetmt

        return render(request,
                'assetmgt/assetmanagement.html',
                context)

def Logout_view(request):
    userv = request.user
    logout(request)
    #addMessage("%s User logged out"%user)

    url = reverse('login')
    return HttpResponseRedirect(url)  
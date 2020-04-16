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
from .forms import AssetMgtForm2
from .views import xlsGenerate

from django.contrib import messages

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
from django.forms import formset_factory



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

# def returnAssetMgtMultiForm(request):
#     """
#     Method returns Service Form
#     """
#     if request.method == 'POST':
#         if 'hospital_id' in request.POST:
#             hid = request.POST['hospital_id']
#             try:
#                 inidict = {}
#                 inidict['hospital_id'] = Hospital.objects.get(hospital_id=hid)
#                 inidict['asset_id'] = ''
#                 assets = Asset.objects.all()
#                 context = {}
#                 context['forms'] = {}
#                 for ast in assets:
#                     try:
#                         objast = AssetMgt.objects.filter(hospital_id=hid,asset_id=ast).last()
#                         total = objast.asset_total
#                     except:
#                         total = 0
#                         pass
#                     inidict['asset_id'] = ast
#                     inidict['asset_total'] = total  
#                     context['forms'][ast.asset_name] = AssetMgtForm2(
#                         initial=inidict,prefix=ast.asset_name)
#                 print(context)
#                 return render(request, 'assetmgt/multiform.html', context)
#             except Exception as details:
#                 print(details)
#                 return HttpResponse("Select Hospital")
#         else:
#             return HttpResponse("Select Hospital")
#     else:
#         return HttpResponse("Select Hospital")


def returnAssetMgtMultiForm(request):
    """
    Method returns Service Form
    """
    if request.method == 'POST':
        if 'hospital_id' in request.POST:
            hid = request.POST['hospital_id']
            try:
                AssetMgtFormset = formset_factory(AssetMgtForm2,extra=0)
                initopass = []                
                assets = Asset.objects.all()
                context = {}
                
                for ast in assets:
                    inidict = {}
                    inidict['hospital_id'] = Hospital.objects.get(hospital_id=hid)
                    inidict['asset_id'] = ''
                    try:
                        objast = AssetMgt.objects.filter(hospital_id=hid,asset_id=ast).last()
                        total = objast.asset_total
                    except:
                        total = 0
                        pass
                    inidict['asset_id'] = ast
                    inidict['asset_total'] = total  
                    initopass.append(inidict)
                    print(initopass)

                formset = AssetMgtFormset(initial=initopass)
                print(dir(formset))
                
                return render(request, 'assetmgt/multiform.html', {
                    'formset':formset,'initdata':initopass,
                    'hospitaln':inidict['hospital_id']
                    })
            except Exception as details:
                print(details)
                return HttpResponse("Select Hospital")
        else:
            return HttpResponse("Select Hospital")
    else:
        return HttpResponse("Select Hospital")


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
def addMultipleAssetManagement(request):
    print("Request has come")
    if request.method == 'POST':
        #print(request.POST)
        try:
            AssetMgtFormset = formset_factory(AssetMgtForm2)
            inid = request.POST['initd']
            formset = AssetMgtFormset(request.POST)
            # for forms in formset:
            #     forms.full_clean()
            if formset.is_valid():
                print("Form is valid")
        
                for form in formset:
                    print(form)
                    obj = form.save(commit=False)
                    if obj.asset_total:
                        obj.author = request.user
                        obj.asset_balance = obj.asset_total - obj.asset_utilized
                        obj.save()
            else:
                print(formset.errors)
                print("Some Issue")
            
                #messages.info(request,'Asset Added')
            messages.info(request,"Data has been Updated")
            url = reverse('assetmanagementview')
            return HttpResponseRedirect(url)
        except IntegrityError as ie:
            print("Asset already exists")
            url = reverse('assetmanagementview')
            messages.info(request,"Issue in Updating ")
            return HttpResponseRedirect(url)
            # return HttpResponse("AE")

        except Exception as details:
            print("adding policy "+str(details))
            messages.info(request,"Issue in Updating ")
            url = reverse('assetmanagementview')
            return HttpResponseRedirect(url)
    url = reverse('assetmanagementview')
    return HttpResponseRedirect(url)




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

            assetmt = AssetMgt.objects.filter(
                hospital_id=user.userprofile.hospital_id.hospital_id
                ).order_by('asset_id','-creation_date').distinct('asset_id')
            sample_tmp=xlsGenerate(assetmt,user.username)
        elif user.userprofile.adminstate == 1:
            print("District admin")
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
            rendered = render_to_string('assetmgt/districtadmin.html', {'hospitals': hosp })
            hids = Hospital.objects.filter(
                        district_id=user.userprofile.district_id.district_id
                        ).values_list('hospital_id',flat=True)
            assetmt = AssetMgt.objects.filter(hospital_id__in=hids)
            assetmt = AssetMgt.objects.filter(hospital_id__in=hids).order_by(
                'asset_id','-creation_date').distinct('asset_id')
            sample_tmp=xlsGenerate(assetmt,user.username)
        else:
            print("State Admin ")
            dist = District.objects.filter(state_id=user.userprofile.state_id.state_id)
            hids = Hospital.objects.filter(
                        state_id=user.userprofile.state_id.state_id
                        ).values_list('hospital_id',flat=True)
            rendered = render_to_string('assetmgt/stateadmin.html', {'dist': dist})
            assetmt = AssetMgt.objects.all().order_by(
                'asset_id','-creation_date').distinct('asset_id')
            sample_tmp=xlsGenerate(assetmt,user.username)

        context = dict()
        

        context['selecthospital'] = rendered
        context['assetmgt'] = assetmt
        context['sample_tmp'] = sample_tmp

        return render(request,
                'assetmgt/assetmanagement.html',
                context)

def Logout_view(request):
    userv = request.user
    logout(request)
    #addMessage("%s User logged out"%user)

    url = reverse('login')
    return HttpResponseRedirect(url) 

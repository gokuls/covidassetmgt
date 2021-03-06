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
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import LoginForm
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

def error_404(request,exception):
        data = {}
        #return render(request,'snippets/404.html', data)
        return render(request,
            'assetmgt/error_page.html',
            {})

def error_500(request):
        data = {}
        return render(request,
            'assetmgt/error_page.html',
            {})


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


def returnCaptcha(request):
    to_json_response = dict()
    to_json_response['key'] = CaptchaStore.generate_key()
    to_json_response['image_url'] = captcha_image_url(to_json_response['key'])
    return JsonResponse(to_json_response)

class AjaxExampleForm(CreateView):
    template_name = ''
    form_class = LoginForm()

    def form_invalid(self, form):
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 0
            to_json_response['form_errors'] = form.errors

            to_json_response['key'] = CaptchaStore.generate_key()
            to_json_response['image_url'] = captcha_image_url(to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response), content_type='application/json')

    def form_valid(self, form):
        form.save()
        if self.request.is_ajax():
            to_json_response = dict()
            to_json_response['status'] = 1

            to_json_response['new_cptch_key'] = CaptchaStore.generate_key()
            to_json_response['new_cptch_image'] = captcha_image_url(to_json_response['new_cptch_key'])

            return HttpResponse(json.dumps(to_json_response), content_type='application/json')

@login_required
def AssetsView(request):
    '''
        Page to view the asset and add the Asset 
    '''
    if request.user.userprofile.adminstate < 2:
        messages.info(request,"You are not Authorised to View this page ")
        return redirect('index')
    assets = Asset.objects.all()
    context = dict()

    context['assets'] = assets

    return render(request,
                 'assetmgt/assetview.html',
                 context)




@login_required
def AssetsMappingView(request):
    '''
        Page to view the asset and add the Asset 
    '''
    if request.user.userprofile.adminstate < 1:
        messages.info(request,"You are not Authorised to View this page ")
        return redirect('index')
    
    context = dict()


    return render(request,
                 'assetmgt/assetmapping.html',
                 context)


def returnhtypeMappingForm(request):
    """
    Method to return Asset Mapping based on Hospital Type
    """
    formtype = request.GET['formt']
    if formtype == "hospitaltype":
        htypes = HospitalType.objects.all()
        context = dict()
        context['htypes'] = htypes
        return render(request,'assetmgt/htypemapping.html',context)
    else:
        user = request.user
        context = dict()
        if user.userprofile.adminstate ==2:
            hosp = Hospital.objects.filter(state_id=user.userprofile.state_id.state_id)
        else:
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
        context['hosp'] = hosp
        return render(request,'assetmgt/hospitalmapping.html',context)

def returnAssetsHt(request):
    """
    """
    #assets = Asset.objects.all()
    context = dict()
    htype = request.GET['ht']
    htypeobj = HospitalType.objects.get(htype_id=int(htype))

    if request.user.userprofile.adminstate ==2:
        exisa = HtypeAssetMapping.objects.filter(
        state=request.user.userprofile.state_id,
        htype=htypeobj).distinct('assetsmapped')

    else:
        exisa = HtypeAssetMapping.objects.filter(
        district=request.user.userprofile.district_id,
        htype=htypeobj).distinct('assetsmapped')

    assetsmappeda = exisa.values_list('assetsmapped',flat=True)
    #print(exisa)
    context['vals'] = Asset.objects.exclude(asset_id__in=assetsmappeda)
    context['existasset'] = exisa
    #context['vals'] = assets - assetsmappeda

    return render(request,'assetmgt/assetval.html',context)

def returnAssetsH(request):
    """
    """
    assets = Asset.objects.all()
    context = dict()
    htype = request.GET['ht']
    hobj = Hospital.objects.get(hospital_id=int(htype))
    exisa = HospAssetMapping.objects.filter(
        hospital=hobj).distinct('assetsmapped')
    assetsmappeda = exisa.values_list('assetsmapped',flat=True)
    context['vals'] = Asset.objects.exclude(asset_id__in=assetsmappeda)
    context['existasset'] = exisa

    return render(request,'assetmgt/assetval.html',context)

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

def returnAssetShow(request):
    """
    Method returns Service Form
    """
    if request.method == 'POST':
        if 'hospital_id' in request.POST:
            hid = request.POST['hospital_id']
            #print(hid)
            try:
                context = dict()

                initopass = []
                hid = Hospital.objects.get(hospital_id=hid)
                assets = Asset.objects.all()
                for ast in assets:
                    inidict = {}
                    try:
                        an =  AssetMgt.objects.filter(hospital_id=hid,asset_id=ast).last()
                        if an:
                            initopass.append(an)
                    except:
                        pass

                totalc = len(initopass)
                if totalc:
                    objdic = dict()
                    itc = 0
                    while(1):
                        objdic[itc] = initopass[itc:itc+4]
                        itc = itc+4
                        if itc > totalc:
                            break
                #print(objdic)
                returnstring = ''
                for key,value in objdic.items():
                    mstring = '''
                    <div class="row"><div class="col-md-12 "><div class="card ">
                    <div class="card-body"> <div class="row"> %s</div></div></div></div></div>
                    '''
                    substr = ''
                    for i in value:
                        #print(i)
                        aname = i.asset_id.asset_name
                        aname = aname.split()
                        aname = "".join(aname)
                        #print(aname)
                        aimage = "static/assetmgt/images/icons/"+aname.lower()+"-b.svg"
                        #print(aimage)
                        try:
                            ival = int( (i.asset_utilized/i.asset_total)*100 )
                        except :
                            ival = 0
                        if ival < 25:
                            cname = 'bg-success'
                        elif ival > 25 and ival < 60:
                            cname = 'bg-warning'
                        else:
                            cname = 'bg-danger'

                        tmpstr = '''
                        <div class="col-md-3 "><div class="card bg-white card-img-holder 
                        text-black text-center"><div class="card-body"> 
                        <img class="mb-2" width="64px;" src="{1}" ><div class="progress mb-2">
                        <div class=" progress-bar {2}" style="width:{3}%"> 
                        {3}%</div></div> </span><h4 class="mb-2"> {0}</h4>
                        </div></div></div>'''.format(aname,aimage,cname,ival)
                        #print(tmpstr)
                        substr = substr + tmpstr
                    mstring = mstring%substr
                    returnstring = returnstring+mstring


                return render(request, 'assetmgt/multiform2.html', {
                    'initdata':initopass,
                    'hospitaln':hid,
                    'cdata' : returnstring,
                    'submessage': "Show Details",
                    'btitle' : "View Hospital Details"
                    })
            except Exception as details:
                print(details)
                return HttpResponse("No Records Found")
        else:
            return HttpResponse("Select Hospital")
    else:
        return HttpResponse("Select Hospital")







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
                #assets = Asset.objects.all()
                hobj = Hospital.objects.get(hospital_id=hid)
                aids = HospAssetMapping.objects.filter(
                    hospital=hobj).values_list('assetsmapped',flat=True)
                assets = Asset.objects.filter(asset_id__in=aids)
                context = {}
                if not assets:
                    return HttpResponse("No Assets Have been Mapped to %s Hospital"%hobj.hospital_name)
                for ast in assets:
                    inidict = {}
                    inidict['hospital_id'] = hobj
                    inidict['asset_id'] = ''
                    try:
                        objast = AssetMgt.objects.filter(hospital_id=hid,asset_id=ast).last()
                        total = objast.asset_total
                        utilized = objast.asset_utilized
                    except:
                        total = 0
                        utilized = 0
                        pass
                    inidict['asset_id'] = ast
                    inidict['asset_total'] = total
                    inidict['asset_utilized'] = utilized  
                    initopass.append(inidict)
                    #print(initopass)

                formset = AssetMgtFormset(initial=initopass)
                #print(dir(formset))
                
                return render(request, 'assetmgt/multiform.html', {
                    'formset':formset,'initdata':initopass,
                    'hospitaln':inidict['hospital_id'],
                    'submessage': "Update Details",
                    'btitle' : "Update Hospital Details"
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
            updateflag = False
            mess = ['<p>']
            if formset.is_valid():
                print("Form is valid")
                
        
                for form in formset:
                    #print(form)
                    try:
                        obj = form.save(commit=False)
                        if obj.asset_total:
                            if obj.asset_utilized <= obj.asset_total:
                                obj.author = request.user
                                obj.asset_balance = obj.asset_total - obj.asset_utilized 
                                obj.save()
                                updateflag = True
                            else:
                                mess.append("Utilization was given more then Total for Asset %s"\
                                    %obj.asset_id.asset_name)
                        else:
                            if obj.asset_utilized > 0:
                                mess.append("Total Should be more then utilized Invalid input for %s"\
                                    %obj.asset_id.asset_name)
                    except Exception:
                        mess.append(" Provide Positve Integer Value ")
            else:
                #print(formset.errors)
                print("Some Issue")
            
                #messages.info(request,'Asset Added')
                mess.append("Provide Valid Values : Values should be Positve Integer and \
                    Utilization should be less then or equal to Total")
            if updateflag:
                mess.append("All Valid Inputs has been Updated")
            mess.append("</p>")
            mes = "</p><p>".join(mess)
            messages.info(request,mes)
            url = reverse('assetmanagementview')

            return HttpResponseRedirect(url)
        except IntegrityError as ie:
            print(ie)
            #print("Asset already exists")
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

def returnData(userobj):
    '''
        return data for constructing Excel
    '''
    # userobj = request.user
    datatowrite = []
    #assetobj = Asset.objects.all()
    hids = []

    if userobj.userprofile.adminstate == 0:
        hosp = Hospital.objects.get(
            hospital_id=userobj.userprofile.hospital_id.hospital_id
            )
    elif userobj.userprofile.adminstate == 1:
        hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
    else:
        hosp = Hospital.objects.filter(state_id=user.userprofile.district_id.district_id)
    
    for i in hosp:
        assetobj=HospAssetMapping.objects.filter(hospital=i).values('assetsmapped')
        for a in assetobj:
            tmp = []
            tmp.append(i.hospital_id)
            tmp.append(i.hospital_name)
            tmp.append(a.asset_name)
            try:
                bjast = AssetMgt.objects.filter(hospital_id=hid,asset_id=ast).last()
                total = objast.asset_total
                utilized = objast.asset_utilized
            except:
                total = 0
                utilized = 0
            tmp.append(total)
            tmp.append(utilized)
            datatowrite.append(tmp)
    #print(datatowrite)
    return datatowrite

"""
    XLS Generate Download
"""
@login_required
def AssetMgmtemDownload(request):
     if request.user:
        user = request.user 
        datatowrite = []
        userobj = user        
        hids = []
        if userobj.userprofile.adminstate == 0:
            hosp = []
            hosp.append(Hospital.objects.get(
                hospital_id=userobj.userprofile.hospital_id.hospital_id
                ))
        elif userobj.userprofile.adminstate == 1:
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
        else:
            hosp = Hospital.objects.filter(state_id=user.userprofile.state_id.state_id)
        
        for i in hosp:            
            assetobj=HospAssetMapping.objects.filter(hospital=i).distinct('assetsmapped')            
            for a in assetobj:
                tmp = []
                tmp.append(i.hospital_id)
                tmp.append(i.hospital_name)
                tmp.append(a.assetsmapped.asset_name)
                try:
                    objast = AssetMgt.objects.filter(hospital_id=i,asset_id=a.assetsmapped).last()
                    total = objast.asset_total
                    utilized = objast.asset_utilized
                except:
                    total = 0
                    utilized = 0
                tmp.append(total)
                tmp.append(utilized)
                datatowrite.append(tmp)        

        wb = xlwt.Workbook(encoding='utf-8') # create empty workbook object
        newsheet = wb.add_sheet('asset_details') # sheet name can not be longer than 32 characters    
        newsheet.write(0,0,'hospital_id') 
        newsheet.write(0,1,'hospital_name')
        newsheet.write(0,2,'Asset_name')
        newsheet.write(0,3,'Total')
        newsheet.write(0,4,'Utilized')
        rows=1    
        for dat in datatowrite:        
            newsheet.write(rows,0,dat[0])
            newsheet.write(rows,1,dat[1])
            newsheet.write(rows,2,dat[2])
            newsheet.write(rows,3,dat[3])
            newsheet.write(rows,4,dat[4])
            rows += 1
        # content-type of response
        response = HttpResponse(content_type='application/ms-excel')
        # file name
        epoc=int(time.time())
        fileName = str(request.user)+"-"+str(epoc)+".xls"        
        response['Content-Disposition'] = 'attachment; filename="%s"' %(fileName)
        wb.save(response)       
        return response

@login_required
def AssetManagementView(request):
    if request.user:
        user = request.user         
        if user.userprofile.adminstate == 0:
            #print('Hospital admin')
            hosp = Hospital.objects.get(hospital_id=user.userprofile.hospital_id.hospital_id)
            rendered = render_to_string('assetmgt/hospitaladmin.html', 
                {'hospitals': hosp, 'submessage': "Update Details",'btitle' : "Update Hospital Details" })

            assetmt = AssetMgt.objects.filter(
                hospital_id=user.userprofile.hospital_id.hospital_id
                ).order_by('asset_id','hospital_id','-creation_date').distinct('asset_id')
            #sample_tmp=xlsGenerate(assetmt,user.username)

        elif user.userprofile.adminstate == 1:
            #print("District admin")
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
            rendered = render_to_string('assetmgt/districtadmin.html', {'hospitals': hosp,
            'submessage': "Update Details",'btitle' : "Update Hospital Details" })
            hids = Hospital.objects.filter(
                        district_id=user.userprofile.district_id.district_id
                        ).values_list('hospital_id',flat=True)
            #assetmt = AssetMgt.objects.filter(hospital_id__in=hids)
            assetmt = []
            for i in hids:
                tmp = AssetMgt.objects.filter(hospital_id=i).order_by(
                'asset_id','-creation_date').distinct('asset_id')
                assetmt.extend(tmp)
            #sample_tmp=xlsGenerate(assetmt,user.username)
        else:
            print("State Admin ")
            dist = District.objects.filter(state_id=user.userprofile.state_id.state_id)
            hids = Hospital.objects.filter(
                        state_id=user.userprofile.state_id.state_id
                        ).values_list('hospital_id',flat=True)
            rendered = render_to_string('assetmgt/stateadmin.html', 
                {'dist': dist,'submessage': "Update Details",'btitle' : "Update Hospital Details"})
            assetmt = []
            for i in hids:
                tmp = AssetMgt.objects.filter(hospital_id=i).order_by(
                'asset_id','-creation_date').distinct('asset_id')
                assetmt.extend(tmp)
            #sample_tmp=xlsGenerate(assetmt,user.username)
        context = dict()           

        context['selecthospital'] = rendered
        context['assetmgt'] = assetmt
        

        return render(request,
                'assetmgt/assetmanagement.html',
                context)
    else:
        return render(request,
                'assetmgt/assetmanagement.html',
                context)

def HospitalTypeAssetMapping(request):
    """

        Map Assets to Hospital Type
        Map Assets to the Hospital 
        Then send response 
    """
    try:
        hosptype = request.POST['htypeid']
        assets = request.POST.getlist('assets')
        if assets:
            assetobjs = [Asset.objects.get(asset_id=int(i)) for i in assets ]
        #print(hosptype)
        #print(assets)
        htypeobj = HospitalType.objects.get(htype_id=int(hosptype))
        with transaction.atomic():
            state = request.user.userprofile.state_id
            
            if request.user.userprofile.adminstate == 2:
                districts = District.objects.filter(state_id=state)
                for dists in districts:
                    for asset in assetobjs:
                        HtypeAssetMapping.objects.create(
                        state = state,
                        district = dists,
                        htype = htypeobj,
                        assetsmapped = asset
                        )
            else:
                district = request.user.userprofile.district_id
                for asset in assetobjs:
                    HtypeAssetMapping.objects.create(
                        state = state,
                        district = district,
                        htype = htypeobj,
                        assetsmapped = asset
                        )

            ## Get hospital List
            if request.user.userprofile.adminstate == 2:
                hospitals = Hospital.objects.filter(state_id=state,htype=htypeobj)
            else:
                hospitals = Hospital.objects.filter(district_id=district,htype=htypeobj)

            for h in hospitals:
                for ast in assetobjs:
                    HospAssetMapping.objects.create(
                        hospital = h,
                        assetsmapped = ast
                        )





        ## get the list of assets. 
        lisofasset = [ ast.asset_name for ast in assetobjs ]
        str1 = " , ".join(lisofasset)
        

        return HttpResponse("Assets : %s mapped to %s"%(str1,htypeobj.hospital_type))

    except Exception as details:
        print(details)
        return HttpResponse("Error")


def HospitalAssetMapping(request):
    """

        Map Assets to Hospital Type
        Map Assets to the Hospital 
        Then send response 
    """
    try:
        hospid = request.POST['hospid']
        assets = request.POST.getlist('assets')
        if assets:
            assetobjs = [Asset.objects.get(asset_id=int(i)) for i in assets ]
        #print(hospid)
        #print(assets)
        
        with transaction.atomic():
            ## Get hospital List
            hospital = Hospital.objects.get(hospital_id=int(hospid))
            for ast in assetobjs:
                HospAssetMapping.objects.create(
                    hospital = hospital,
                    assetsmapped = ast
                    )



        ## get the list of assets. 
        lisofasset = [ ast.asset_name for ast in assetobjs ]
        str1 = " , ".join(lisofasset)
        

        return HttpResponse("Assets : %s mapped to %s"%(str1,
            Hospital.objects.get(hospital_id=int(hospid)).hospital_name))

    except Exception as details:
        print(details)
        return HttpResponse("Error")



def AssetManagementImgView(request):
    if request.user:
        user = request.user 
        if user.userprofile.adminstate == 0:
            print('Hospital admin')
            hosp = Hospital.objects.get(hospital_id=user.userprofile.hospital_id.hospital_id)
            rendered = render_to_string('assetmgt/hospitaladmin.html', {'hospitals': hosp,
                'submessage': "Show Details",'btitle' : "View Hospital Details" })

            assetmt = AssetMgt.objects.filter(
                hospital_id=user.userprofile.hospital_id.hospital_id
                ).order_by('asset_id','-creation_date').distinct('asset_id')

        elif user.userprofile.adminstate == 1:
            print("District admin")
            hosp = Hospital.objects.filter(district_id=user.userprofile.district_id.district_id)
            rendered = render_to_string('assetmgt/districtadmin.html', {'hospitals': hosp,
            'submessage': "Show Details",'btitle' : "View Hospital Details" })
            hids = Hospital.objects.filter(
                        district_id=user.userprofile.district_id.district_id
                        ).values_list('hospital_id',flat=True)
            #assetmt = AssetMgt.objects.filter(hospital_id__in=hids)
            assetmt = AssetMgt.objects.filter(hospital_id__in=hids).order_by(
                'asset_id','-creation_date').distinct('asset_id')
            
        else:
            print("State Admin ")
            dist = District.objects.filter(state_id=user.userprofile.state_id.state_id)
            hids = Hospital.objects.filter(
                        state_id=user.userprofile.state_id.state_id
                        ).values_list('hospital_id',flat=True)
            rendered = render_to_string('assetmgt/stateadmin.html', {'dist': dist,
                'submessage': "Show Details",'btitle' : "View Hospital Details"})
            assetmt = AssetMgt.objects.filter(hospital_id__in=hids).order_by(
                'asset_id','-creation_date').distinct('asset_id')

        context = dict()
        

        context['selecthospital'] = rendered
        context['assetmgt'] = assetmt

        return render(request,
                'assetmgt/assetmanagement-img.html',
                context)


def Logout_view(request):
    userv = request.user
    logout(request)
    #addMessage("%s User logged out"%user)

    url = reverse('login')
    return HttpResponseRedirect(url) 

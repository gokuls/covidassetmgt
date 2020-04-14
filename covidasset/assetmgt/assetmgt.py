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
from django.views.generic.edit import CreateView
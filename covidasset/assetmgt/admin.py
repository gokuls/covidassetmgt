from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(State)
admin.site.register(District)
admin.site.register(Hospital)
admin.site.register(Asset)
admin.site.register(AssetMgt)
admin.site.register(PatientStat)
admin.site.register(UserProfile)

admin.site.register(HospitalType)


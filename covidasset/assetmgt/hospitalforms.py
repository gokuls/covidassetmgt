from django.forms import ModelForm
from django import forms
from assetmgt.models import Hospital,District,State

class HospitalForm(ModelForm):
    class Meta:
        model = Hospital
        fields = ['hospital_name','hospital_type','address','contact_number','doctors','healthworkers','latitude','longitude']
        def __init__(self, *args, **kwargs):
            user = kwargs.pop('user','')
            super(HospitalForm, self).__init__(*args, **kwargs)
            self.fields['state']=forms.ModelChoiceField(queryset=State.objects.filter(state_id=stateid))
            self.fileds['district']=forms.ModelChoiceField(queryset=District.objects.filter(district_id=districtid))




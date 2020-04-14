from  django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import District
from .models import Hospital
from .models import Asset
from .models import AssetMgt
from django.forms import TextInput
from django.forms import PasswordInput



CATE = ((0,"Hospital Admin"),(1,"District Admin"),(2,"State Admin"))

class LoginForm(forms.Form):
        username = forms.CharField(
				widget=forms.TextInput(attrs={'class':'form-control'}), 
				help_text='Enter User Name')
        password = forms.CharField(
				label='Password', 
				widget=forms.PasswordInput(
					attrs={'class':'form-control','autocomplete':'off'}), 
				help_text='Enter Password')



class ExtendedUserCreationForm(UserCreationForm):
	first_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)


	class Meta:
		model = User 
		fields = ('username','first_name','last_name','password1','password2')

	def save(self, commit=True):
		user = super().save(commit=False)

		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['first_name']

		if commit:
			user.save()
		return user


class AssetForm(forms.ModelForm):
	asset_name = forms.CharField(max_length=150)
	


	class Meta:
		model = Asset 
		fields = ('asset_name',)
		



class HospitalForm(forms.ModelForm):
	class Meta:
		model = Hospital
		fields = ('state_id','hospital_id', 'district_id','hospital_name',
				'hospital_type', 'address', 'contact_number',
					'city','taluk','pincode', 'doctors', 'healthworkers', 'latitude',
				'longitude')




class AssetMgtForm(forms.ModelForm):
	#hospital_id = forms.HiddenInput()

	class Meta:
		model  = AssetMgt
		fields = ('asset_id','asset_total','asset_utilized','hospital_id')
		# widgets = {
		# 		'hospital_id' :  forms.HiddenInput()
		# }

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# print("In Form Creation")
		# print(kwargs)
		# self.fields['hospital_id'].queryset = Hospital.objects.get(
		# 			hospital_id=kwargs['initial']['hospital_id'].hospital_id)

		#print(self.fields['hospital_id'])




class UserProfileForm(forms.ModelForm):
	adminstate = forms.ChoiceField(choices = CATE)

	class Meta:
		model = UserProfile
		fields = ('state_id','district_id','hospital_id','adminstate')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['district_id'].queryset = District.objects.none()
		self.fields['hospital_id'].queryset = Hospital.objects.none()


		if 'state_id' in self.data:
			try:
				state_id = int(self.data.get('state_id'))
				self.fields['district_id'].queryset = District.objects.filter(
								state_id=state_id).order_by('district_name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['district_id'].queryset = self.instance.state.district_set.order_by(
												'district_name')


		if 'district_id' in self.data:
			try:
				district_id = int(self.data.get('district_id'))
				self.fields['hospital_id'].queryset = Hospital.objects.filter(
					district_id=district_id).order_by('hospital_name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			#self.fields['district_id'].queryset = self.instance.state.district_set.order_by('district_name')
			self.fields['hospital_id'].queryset = self.instance.district.hospital_set.order_by(
												'hospital_name')

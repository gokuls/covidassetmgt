from  django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile
from .models import District


CATE = ((0,"Hospital Admin"),(1,"District Admin"),(2,"State Admin"))

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

class UserProfileForm(forms.ModelForm):
	adminstate = forms.ChoiceField(choices = CATE)

	class Meta:
		model = UserProfile
		fields = ('state_id','district_id','hospital_id','adminstate')

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['district_id'].queryset = District.objects.none()


		if 'state_id' in self.data:
			try:
				state_id = int(self.data.get('state_id'))
				self.fields['district_id'].queryset = District.objects.filter(state_id=state_id).order_by('district_name')
			except (ValueError, TypeError):
				pass  # invalid input from the client; ignore and fallback to empty City queryset
		elif self.instance.pk:
			self.fields['district_id'].queryset = self.instance.state.district_set.order_by('district_name')
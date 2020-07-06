from .models import UserProfile
from django.conf import settings
from django import forms



# class UserForm(forms.ModelForm):
	# confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	# confirm_password.widget.attrs.update({'class' : 'form-control'})

	# class Meta():
	# 	model = settings.AUTH_USER_MODEL
	# 	fields = ('email', 'password', 'confirm_password')
	# 	widgets = {

	# 		'email': forms.TextInput( attrs = {
	# 			'class' : 'form-control'
	# 		}),

	# 		'password': forms.PasswordInput( attrs = {
	# 			'class' : 'form-control'
	# 		})

	# 	}



class InternForm(forms.ModelForm):
	password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	password.widget.attrs.update({'class' : 'form-control'})
	confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)
	email = forms.EmailField(widget=forms.EmailInput)
	email.widget.attrs.update({'class' : 'form-control'})
	confirm_password.widget.attrs.update({'class' : 'form-control'})

	class Meta():
		model = UserProfile
		fields =  ('first_name', 'last_name', 'email', 'password', 'confirm_password')
		widgets = {
			'first_name': forms.TextInput( attrs = {
				'class' : 'form-control'
			}),
			
			'last_name': forms.TextInput( attrs = {
				'class' : 'form-control'
			}),
			
			'email': forms.EmailInput( attrs = {
				'class' : 'form-control'
			}),

			'password': forms.PasswordInput( attrs = {
				'class' : 'form-control'
			})
		}

	def clean_last_name(self):
		last_name = self.cleaned_data.get('last_name')

		if len(last_name) < 3:
			raise forms.ValidationError('Size less than 3')

		return last_name 

	def clean_first_name(self):
		first_name = self.cleaned_data.get('first_name')

		if len(first_name) < 3:
			raise forms.ValidationError('Size less than 3')

		return first_name 



	def clean_confirm_password(self):
		password = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')

		if password != confirm_password :
			raise forms.ValidationError(f'Password does not match{confirm_password} {password}') 
		
		return password 

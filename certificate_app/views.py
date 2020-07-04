from django.shortcuts import render, redirect, reverse
from .forms import  InternForm
from .models import UserProfile, Profile
from django.conf import settings
# import smtplib
import threading
from .functions import send_email, save_user, delete_inactive, generate_token, delete_user_inactive, change_token, get_intern
import threading
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  authenticate, login as auth_login , logout
from django.contrib import messages
from .decorators import is_admin, is_intern
from django.contrib.auth import get_user_model
# Create your views here.


def register_user(request):
	''' registration of interns '''

	# delete inactive user
	# form = UserForm(None)
	form = InternForm(None)

	if request.method == 'POST':
		# form = UserForm(request.POST)
		form = InternForm(request.POST)
		# user = User.objects.all().filter(email='jhabarsinghbhati23@gmail.com').first()
		# Profile.objects.all().filter(user=user).first().delete()
		# user.delete()
		delete_inactive(request.POST.get('email'))
		if form.is_valid():
			if not get_user_model().objects.all().filter(email=request.POST.get('email')).first():
				save_user(request.POST)

				# id = User.objects.all().filter(email=request.POST.get('email')).first().id
				# full_name = request.POST.get('first_name')+' '+request.POST.get('last_name')
				# thread = threading.Thread(target=send_email, args=(full_name, id, request.POST.get('email')))

				thread1 = threading.Thread(target=delete_user_inactive, args=(request.POST.get('email'),))
				# thread.start()
				thread1.start()
				# send_email(full_name, id, request.POST.get('email'))
				return redirect(reverse('certificate_app:register_activation'))
			messages.error(request, 'User Name Already Exist')
	return render(request, 'register.html', context={'form': form})


def login(request):
	''' login user '''
	
	if request.method == "POST":
		email = request.POST.get("email")
		password = request.POST.get("password")
		profile = Profile.objects.all().filter(intern=get_intern(email)).first()
		if get_user_model().objects.all().filter(email=email).first():
			user = authenticate(request, email=email,
									password = password)
			if user and get_user_model().objects.all().filter(email=email).first().is_superuser:
					auth_login(request, user)
					return redirect(reverse("certificate_app:admin_dashboard"))
		if profile:
			if profile.is_active:
				user = authenticate(request, email=email,
									password = password)
				print('$$$$$$$$$$$$$$$$')
				if user:
					if user.is_active:
						auth_login(request, user)	
						id = user.id
						return redirect(reverse("certificate_app:personal_details"))
					else:
						messages.error(request, "Not A Active User")			
				
	return render(request, "login.html")


# def login_admin(request):
# 	''' login admin '''
	
# 	if request.method == "POST":
# 		email = request.POST.get("email")
# 		password = request.POST.get("password")

# 		user = authenticate(request, email=email,
# 							password = password)
# 		if user:
# 			if user.is_superuser:
# 				auth_login(request, user)	
# 				return redirect(reverse("certificate_app:admin_dashboard"))
# 			else:
# 				messages.error(request, "Not A Admin User")			
# 		else:
# 				messages.error(request, "Invalid Credentials")
# 	return render(request, "admin_login.html")


# @login_required
# def logout_user(request):
# 	''' logout user'''

# 	return render(request, 'logout.html')


@login_required
def confirm_logout_user(request):
	
	if request.POST.get("ok" or None):
		logout(request)
		return redirect(reverse("certificate_app:login"))
	if request.POST.get("cancel" or None):
		return redirect(reverse("certificate_app:personal_details")) 

	return render(request, "confirm_logout.html")


def register_activation(request):
	''' link open when user regiters and email is sent to his/her Id
		displays that got to your email to authenticate
	'''

	return render(request, 'register_activation.html')


def register_token(request, key):
	'''	verifies if the given activation key is valid or not
	'''
	profile = Profile.objects.all().filter(activation_key=key).first()

	if profile:
		print(profile.intern)
		Profile.objects.all().filter(activation_key=key).update(is_active=True)
		Profile.objects.all().filter(activation_key=key).update(activation_key=generate_token())

		return redirect(reverse('certificate_app:login'))
	return render(request, 'register_token.html', context={'data': key})



def forgot_password(request):
	''' forgot password logic '''
	if request.POST.get('email'):
		if get_user_model().objects.all().filter(email=request.POST.get('email')).first():
			send_email(None, None, request.POST.get('email'),True)
			thread1 = threading.Thread(target=change_token, args=(request.POST.get('email'),))
			thread1.start()
			return render(request, 'forgot_password_activation.html')
	return render(request, 'forgot_password.html')


def forgot_password_confirm(request, key):

	profile = Profile.objects.all().filter(activation_key=key).first()
	print("######################\n")
	if profile:
		print("######################\n")
		password = request.POST.get('new_password')
		new_password = request.POST.get('confirm_new_password')
		print( password is new_password , '\n')
		if password and password == new_password:
			profile.intern.user.set_password(password)
			profile.intern.user.save()
			Profile.objects.all().filter(activation_key=key).update(activation_key=generate_token())
			
			return redirect(reverse('certificate_app:login'))
	return render(request, 'new_password.html')


@login_required
@is_intern
def intern_certificate(request, id):
	''' link is opened when intern clicks on certificate
	'''

	return render(request, 'admin/certificate.html')


@login_required
@is_intern
def  personal_details(request):
	''' personal details of intern '''

	return render(request, 'intern/personal_details.html')


@login_required
@is_intern
def  project_details(request):
	'''  project of intern '''

	return render(request, 'intern/project_details.html', context={'data': id})


@login_required
@is_intern
def  report_submission(request):
	''' submission details of intern '''

	return render(request, 'intern/report_submission.html', context={'data': id})


@login_required
@is_admin
def admin_dashboard(request):
	''' admin dashboard'''

	return render(request, 'admin/dashboard.html')


@login_required
@is_admin
def admin_iframe(request):	
	''' admin iframe '''

	return render(request, 'admin/iframe.html')

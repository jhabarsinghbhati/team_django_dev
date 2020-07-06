from django.shortcuts import redirect, reverse
from .models import UserProfile
from django.contrib.auth import get_user_model

def is_admin(fun):
	def authorized(request, *args, **kwargs):
		if request.user.is_authenticated:
			if request.user.is_superuser or get_user_model().is_irscdmin:
					return fun(request, *args, **kwargs)
			else:
				return redirect(reverse('certificate_app:register'))
		else:
			return redirect(reverse("certificate_app:login"))		


	return authorized


def is_intern(fun):
	def authorized(request, *args, **kwargs):
		if UserProfile.objects.all().filter(user=request.user).first():
			if not request.user.is_superuser or get_user_model().is_irscdmin:
				return fun(request, *args, **kwargs)
			else:
				return redirect(reverse('certificate_app:login'))
		else:
			return redirect(reverse("certificate_app:login"))		

	return authorized
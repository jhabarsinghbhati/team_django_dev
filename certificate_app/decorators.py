from django.shortcuts import redirect, reverse
from .models import UserProfile

def is_admin(fun):
	def authorized(request):
		if request.user.is_authenticated:
			if UserProfile.objects.all().filter(user=request.user).first():
				if UserProfile.objects.all().filter(user=request.user).first().is_admin:
					return fun(request)
				return redirect(reverse('certificate_app:login'))
			else:
				return redirect(reverse('certificate_app:register'))
		else:
			return redirect(reverse("certificate_app:login"))		


	return authorized


def is_intern(fun):
	def authorized(request, *args, **kwargs):
		if UserProfile.objects.all().filter(user=request.user).first():
			if not UserProfile.objects.all().filter(user=request.user).first().is_admin:
				return fun(request, *args, **kwargs)
			else:
				return redirect(reverse('certificate_app:login'))
		else:
			return redirect(reverse("certificate_app:login"))		

	return authorized
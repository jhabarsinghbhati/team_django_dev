from django.shortcuts import redirect, reverse


def is_admin(fun):
	def authorized(request):
		if request.user.is_superuser:
			return fun(request)
		else:
			return redirect(reverse("certificate_app:login"))		

	return authorized


def is_intern(fun):
	def authorized(request, *args, **kwargs):
		if not request.user.is_superuser:
			return fun(request, *args, **kwargs)
		else:
			return redirect(reverse("certificate_app:login"))		

	return authorized
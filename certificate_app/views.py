import os
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from datetime import datetime, timedelta
from django.core.files import File
from django.http import JsonResponse
from django.conf import settings

from .certificate import generate_certificate
from .models import Report, Project, Certificate, User, UserProfile, Profile
from .forms import ReportSubmissionForm, PersonalDetailForm, ProjectDetailsForm


from django.shortcuts import render, redirect, reverse
from .forms import InternForm
# from .models import UserProfile, Profile
from django.conf import settings
# import smtplib
import threading
from .functions import send_email, save_user, delete_inactive, generate_token, delete_user_inactive, change_token, get_intern
import threading
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .decorators import is_admin, is_intern
from django.contrib.auth import get_user_model
# Create your views here.


def register_user(request):
    ''' registration of interns '''
    if request.user.is_authenticated:
            if UserProfile.objects.all().filter(user=request.user):
                if UserProfile.objects.all().filter(user=request.user).first().is_admin:
                    return redirect(reverse('certificate_app:mentor'))
                return redirect(reverse('certificate_app:personal_detail'))
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
    if request.user.is_authenticated:
            if UserProfile.objects.all().filter(user=request.user):
                if UserProfile.objects.all().filter(user=request.user).first().is_admin:
                    return redirect(reverse('certificate_app:mentor'))
                return redirect(reverse('certificate_app:personal_detail'))
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile = Profile.objects.all().filter(intern=get_intern(email)).first()
        if get_user_model().objects.all().filter(email=email).first():
            user = authenticate(request, email=email,
                                    password = password)
            if user and get_user_model().objects.all().filter(email=email).first().is_superuser:
                    auth_login(request, user)
                    return redirect(reverse("certificate_app:mentor"))
        if profile:
            if profile.is_active:
                user = authenticate(request, email=email,
                                    password = password)
                print('$$$$$$$$$$$$$$$$')
                if user:
                    if user.is_active:
                        auth_login(request, user)   
                        id = user.id
                        return redirect(reverse("certificate_app:personal_detail"))
                    else:
                        messages.error(request, "Not A Active User")            
                
    return render(request, "login.html")


# def login_admin(request):
#   ''' login admin '''
    
#   if request.method == "POST":
#       email = request.POST.get("email")
#       password = request.POST.get("password")

#       user = authenticate(request, email=email,
#                           password = password)
#       if user:
#           if user.is_superuser:
#               auth_login(request, user)   
#               return redirect(reverse("certificate_app:mentor"))
#           else:
#               messages.error(request, "Not A Admin User")         
#       else:
#               messages.error(request, "Invalid Credentials")
#   return render(request, "admin_login.html")


# @login_required
# def logout_user(request):
#   ''' logout user'''

#   return render(request, 'logout.html')


@login_required
def confirm_logout_user(request):
    # if request.user.is_authenticated:
    #       if UserProfile.objects.all().filter(user=request.user):
    #           if UserProfile.objects.all().filter(user=request.user).is_admin:
    #               return redirect(request, 'certificate_app:mentor')
    #           else:
    #               return redirect(request, 'certificate_app:personal_detail')

    if request.POST.get("ok" or None):
        logout(request)
        return redirect(reverse("certificate_app:login"))
    if request.POST.get("cancel" or None):
        return redirect(reverse("certificate_app:personal_detail")) 

    return render(request, "confirm_logout.html")


def register_activation(request):
    ''' link open when user regiters and email is sent to his/her Id
        displays that got to your email to authenticate
    '''

    return render(request, 'register_activation.html')


def register_token(request, key):
    ''' verifies if the given activation key is valid or not
    '''
    profile = Profile.objects.all().filter(activation_key=key).first()

    if profile:
        print(profile.intern)
        Profile.objects.all().filter(activation_key=key).update(is_active=True)
        Profile.objects.all().filter(activation_key=key).update(activation_key=generate_token())

        return redirect(reverse('certificate_app:login'))
    return render(request, 'register_token.html', context={'data': key})



def forgot_password(request):
    if request.user.is_authenticated:
            if UserProfile.objects.all().filter(user=request.user):
                if UserProfile.objects.all().filter(user=request.user).first().is_admin:
                    return redirect(reverse('certificate_app:mentor'))
                return redirect(reverse('certificate_app:personal_detail'))
    ''' forgot password logic '''
    if request.POST.get('email'):
        if get_user_model().objects.all().filter(email=request.POST.get('email')).first():
            send_email(None, None, request.POST.get('email'),True)
            thread1 = threading.Thread(target=change_token, args=(request.POST.get('email'),))
            thread1.start()
            return render(request, 'forgot_password_activation.html')
    return render(request, 'forgot_password.html')


def forgot_password_confirm(request, key):
    if request.user.is_authenticated:
            if UserProfile.objects.all().filter(user=request.user):
                if UserProfile.objects.all().filter(user=request.user).first().is_admin:
                    return redirect(reverse('certificate_app:mentor'))
                return redirect(reverse('certificate_app:personal_detail'))

    profile = Profile.objects.all().filter(activation_key=key).first()
    print("######################\n")
    if profile:
        print("######################\n")
        password = request.POST.get('new_password') or ''
        new_password = request.POST.get('confirm_new_password') or ''
        print( password is new_password , '\n')
        if password and password == new_password and len(password) >=    8  :
            profile.intern.user.set_password(password)
            profile.intern.user.save()
            Profile.objects.all().filter(activation_key=key).update(activation_key=generate_token())
            return redirect(reverse('certificate_app:login'))
        elif len(password) < 8 and password != '':
            messages.error(request, 'Invalid Password')
    return render(request, 'new_password.html')


# -------------------------------------------------------------------------------------------------

@is_intern
@login_required
def personaldetail(request):
    if request.method == 'POST':
        form = PersonalDetailForm(request.POST, request.FILES)
        if form.is_valid():
            print("form is valid --------------------")
            form.instance.user = request.user
            form.save()
            return redirect('certificate_app:project')
        return render(request, 'personaldetail/detail.html', {'form': form})
    if hasattr(request.user, 'personaldetail'):
        # print("has personal details -------------------------")
        context = {
            'details': request.user.personaldetail
        }
    else:
        form = PersonalDetailForm()
        context = {
            'form': form
        }
    return render(request, 'personaldetail/detail.html', context=context)

@is_intern
@login_required
def personaldetailupdate(request):
    if request.method == 'GET':
        personaldetail = request.user.personaldetail
        form = PersonalDetailForm(instance=personaldetail)
        return render(request, 'personaldetail/detailupdate.html', {'form': form})
    elif request.method == 'POST':
        personaldetail = request.user.personaldetail
        form = PersonalDetailForm(request.POST, instance=personaldetail)
        if form.is_valid():
            form.save()
            return redirect('certificate_app:personal_detail')
        return render(request, 'personaldetail/detailupdate.html', {'form': form})
# -----------------------------------------------------------------------

@is_intern
@login_required
def project(request):
    if request.method == 'POST':
        form = ProjectDetailsForm(request.POST)
        if form.is_valid():
            print("form is valid --------------------")
            form.instance.user = request.user
            form.save()
            return redirect('certificate_app:report')
        # print('form invalid',form.errors)
        return render(request, 'project/project.html', {'form': form})
    if hasattr(request.user, 'project'):
        # print("has personal details -------------------------")
        context = {
            'project': request.user.project
        }
    else:
        form = ProjectDetailsForm()
        context = {
            'form': form
        }
    return render(request, 'project/project.html', context=context)

@is_intern
@login_required
def projectupdate(request):
    if request.method == 'GET':
        project = request.user.project
        form = ProjectDetailsForm(instance=project)
        return render(request, 'project/projectupdate.html', {'form': form})
    elif request.method == 'POST':
        project = request.user.project
        form = ProjectDetailsForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('certificate_app:project')
        return render(request, 'project/projectupdate.html', {'form': form})


# --------------------------------------------------------------------------------
@is_intern
@login_required
def reportview(request):
    if request.method == 'POST':
        form = ReportSubmissionForm(request.POST, request.FILES)
        if form.is_valid:
            form.instance.user = request.user
            form.save()
            return redirect('certificate_app:report')
        return render(request, 'report/report.html', {'from': form})
    form = ReportSubmissionForm()
    return render(request, 'report/report.html', {'form': form})


@is_intern
@login_required
def reportupdate(request):
    if request.method == 'GET':
        report = request.user.report
        form = ReportSubmissionForm(instance=report)
        return render(request, 'report/reportupdate.html', {'form': form})
    elif request.method == 'POST':
        report = request.user.report
        form = ReportSubmissionForm(
            request.POST, request.FILES, instance=report)
        if form.is_valid():
            form.instance.status = "P"
            form.save()
            return redirect('certificate_app:report')
        return render(request, 'report/reportupdate.html', {'form': form})


# ---------------------------------------------------------------------------
@is_admin
@login_required
def adminpage(request):
    if request.user.is_staff:
        get = request.GET.get
        if(get('reg_number')):
            user = User.objects.filter(
                userprofile__registration_number=get('reg_number').strip())
        elif(get('first_name')):
            user = User.objects.filter(
                userprofile__first_name__iexact=get('first_name').strip())
        elif(get('last_name')):
            user = User.objects.filter(
                userprofile__last_name__iexact=get('last_name').strip())
        elif(get('days_from_now')):
            days = int(get('days_from_now').strip())
            user = User.objects.filter(project__end_date__gte=datetime.now(
            ), project__end_date__lt=datetime.now()+timedelta(days=days))
        else:
            user = User.objects.all()
        return render(request, 'admin/adminpage.html', {'user': user})
    raise PermissionDenied()

@is_admin
@login_required
def create_certificate(request, pk):
    if request.user.is_staff:
        intern = get_object_or_404(User, id=pk)
        try:
            intertype = intern.personaldetail.type_of_internship
            profile = intern.personaldetail.profile
            logo = intern.personaldetail.project
            name = intern.userprofile.get_full_name()
            renumber = intern.userprofile.registration_number
        except:
            return JsonResponse({'message': 'Intern has not proper personal details'}, status=404)

        try:
            start_date = intern.project.joining_date
            end_date = intern.project.end_date
        except:
            return JsonResponse({'message': 'Intern has not proper project details'}, status=404)

        if not hasattr(intern, 'certificate'):
            c = Certificate(user=intern)

            filepath = os.path.join(settings.BASE_DIR, 'certificate_file')
            # savepath = os.path.join(settings.MEDIA_ROOT, 'certificates')
            print(logo)
            logo = 'logo'

            png, pdf = generate_certificate(
                filepath, name, intertype, profile, start_date, end_date, logo, renumber)

            c.certificate_pdf.save(
                f'certificate_{renumber}.pdf', File(open(pdf, 'rb')), save=False)
            c.certificate_png.save(
                f'certificate_{renumber}.png', File(open(png, 'rb')), save=True)
            os.remove(png)
            os.remove(pdf)
            # return HttpResponse(f'<div>certificate created successfully with cf no - <a href="{c.certificate_pdf.url}" >{c.certificate_pdf}</a></div>')
            data = {
                'pdfurl': c.certificate_pdf.url,
                'pngurl': c.certificate_png.url,
            }
            return JsonResponse(data)
        return JsonResponse({'message': 'either report not made or certificate already created'}, status=404)
    raise PermissionDenied()

@is_intern
@login_required
def change_status(request, pk):
    if request.user.is_staff:
        value = request.GET.get('status')
        # url = request.GET.get('next')
        try:
            report = get_object_or_404(User, id=pk).report
        except:
            return JsonResponse({'message': 'intern has not report submitted'}, status=404)
        # report = User.objects.get(id=pk).report
        report.status = value
        report.save()
        data = {
            'status': 'status changed successfully'
        }
        return JsonResponse(data)
        # if url:
        #     return redirect(url)
        # return redirect('certificate_app:interndetail',pk=pk)
    raise PermissionDenied

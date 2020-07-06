import random
from .models import UserProfile, Profile
from django.conf import settings
from django.contrib.auth import get_user_model
# import smtplib
import time
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMessage

def delete_inactive(email):
    users = get_user_model().objects.all().filter(email=email).first()
    if users:
        print('delete inactive --------------------------------------')
        intern = UserProfile.objects.all().filter(user=users).first()
        profile = Profile.objects.all().filter(intern=intern).first()
        if profile:
            if not profile.is_active:
                users.delete()


def save_user(data):
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')
    get_user_model().objects.create_user(
        email,
        password
    )

    user = get_user_model().objects.all().filter(email=email).first()
    if user:
        print('save inactive --------------------------------------')
        UserProfile.objects.create(
        user=user, first_name=first_name, last_name=last_name)


def get_intern(email):
    users = get_user_model().objects.all().filter(email=email).first()
    intern = UserProfile.objects.all().filter(user=users).first()
    return intern


def delete_user_inactive(email):
    time.sleep(60*60)
    user = User.objects.all().filter(email=email).first()
    profile = Profile.objects.all().filter(user=user).first().is_active
    if profile:
        pass
    else:
        # Profile.objects.all().filter(user=user).first().delete()
        user.delete()


def change_token(email):
    time.sleep(60*60)
    Profile.objects.all().filter(intern=get_intern(
        email)).update(activation_key=generate_token())


def send_email(name, id, email, forgot_password=False):
    # if not forgot_password:
    # 	token = generate_token()
    # 	user = User.objects.all().filter(email=email).first()
    # 	Profile.objects.create(user=user, activation_key=token)
    token = Profile.objects.all().filter(
        intern=get_intern(email)).first().activation_key

    if forgot_password:
        url = settings.FP_TOKEN_URL
        subject = 'Change Password'
        # user = User.objects.all().filter(email=email).first()
        # token = Profile.objects.all().filter(user=user).first().activation_key
        html_message = render_to_string('mail/forgot.html', {'name': name, 'url': url+'/'+token })
        
        # body = f'Click On The Link To Change Your Password \n\n {url}/{token} \n\n URL Valid only for 1 hour'
    else:
        url = settings.TOKEN_URL
        subject = "Email Verification"
        html_message = render_to_string('mail/register.html', {'name': name, 'id': id, 'email': email, 'url': url+'/'+token})
        # body = strip_tags(html_message)

    # send_mail(
    #     subject,
    #     body,
    #     settings.EMAIL,
    #     [email],
    #     fail_silently=False,
    # )
    message = EmailMessage(subject, html_message, settings.EMAIL, [email])
    message.content_subtype = 'html' # this is required because there is no plain text email message
    message.send()



def welcoming_message(user):
    subject = "Thank You For Registration"
    html_message = render_to_string('mail/thanking.html', {'name': user})
    body = strip_tags(html_message)
    send_mail(
        subject,
        body,
        settings.EMAIL,
        [user.user.email],
        fail_silently=False,
    )


def generate_token():
    alphabets = "abcdefghijklmnopqrstuvwxyz"
    numericals = '0123456789'
    alphanumericals = alphabets+alphabets.upper()+numericals
    length = len(alphanumericals)
    token = ''
    for i in range(64):
        token += alphanumericals[random.randint(0, length-1)]
    return token

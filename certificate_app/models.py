# from django.contrib.auth.models import (
#     AbstractBaseUser, BaseUserManager, PermissionsMixin
# )
from django.db import models
from django.conf import settings
# from django.utils import timezone
# from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import random
import string

# class UserManager(BaseUserManager):
#     def create_user(
#             self, email, first_name, last_name, password=None,
#             commit=True):
#         """
#         Creates and saves a User with the given email, first name, last name
#         and password.
#         """
#         if not email:
#             raise ValueError(_('Users must have an email address'))
#         if not first_name:
#             raise ValueError(_('Users must have a first name'))
#         if not last_name:
#             raise ValueError(_('Users must have a last name'))

#         user = self.model(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#         )

#         user.set_password(password)
#         if commit:
#             user.save(using=self._db)
#         return user

#     def create_superuser(self, email, first_name, last_name, password):
#         """
#         Creates and saves a superuser with the given email, first name,
#         last name and password.
#         """
#         user = self.create_user(
#             email,
#             password=password,
#             first_name=first_name,
#             last_name=last_name,
#             commit=False,
#         )
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(
#         verbose_name=_('email address'), max_length=255, unique=True
#     )
#     # password field supplied by AbstractBaseUser
#     # last_login field supplied by AbstractBaseUser
#     first_name = models.CharField(_('first name'), max_length=30, blank=True)
#     last_name = models.CharField(_('last name'), max_length=150, blank=True)

#     is_active = models.BooleanField(
#         _('active'),
#         default=True,
#         help_text=_(
#             'Designates whether this user should be treated as active. '
#             'Unselect this instead of deleting accounts.'
#         ),
#     )
#     is_staff = models.BooleanField(
#         _('staff status'),
#         default=False,
#         help_text=_(
#             'Designates whether the user can log into this admin site.'
#         ),
#     )
#     # is_superuser field provided by PermissionsMixin
#     # groups field provided by PermissionsMixin
#     # user_permissions field provided by PermissionsMixin

#     date_joined = models.DateTimeField(
#         _('date joined'), default=timezone.now
#     )

#     objects = UserManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['first_name', 'last_name']

#     def get_full_name(self):
#         """
#         Return the first_name plus the last_name, with a space in between.
#         """
#         full_name = '%s %s' % (self.first_name, self.last_name)
#         return full_name.strip()

#     def __str__(self):
#         return '{} <{}>'.format(self.get_full_name(), self.email)

#     def has_perm(self, perm, obj=None):
#         "Does the user have a specific permission?"
#         # Simplest possible answer: Yes, always
#         if self.is_active:
#             return True
#         return False

#     def has_module_perms(self, app_label):
#         "Does the user have permissions to view the app `app_label`?"
#         # Simplest possible answer: Yes, always
#         if self.is_active:
#             return True
#         return False





'''
    From Here Our Project Starts
'''
PROJECT_CHOICE = [
    ('emp1','Exm1'),
    ('emp2','Exm2')
]
PROFILE_CHOICE = [
    ('emp1','Exm1'),
    ('emp2','Exm2')
]
TYPE_OF_INTERNSHIP = [
    ('emp1','Exm1'),
    ('emp2','Exm2')
]
TENURE_CHOICE = [
    ('emp1','Exm1'),
    ('emp2','Exm2')
]

PROFILE = [
    ('FR', 'Freshman'),
    ('SO', 'Sophomore'),
    ('JR', 'Junior'),
    ('SR', 'Senior'),
    ('GR', 'Graduate'),
]

STATUS = [
	('V', 'Volunteer'),
	('I', 'Intern')
]

PROJECT_STATUS = [
	('A', 'Approved'),
	('P', 'Pending'),
	('R', 'Rejected')
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    registration_number = models.CharField(max_length=225,editable=False,unique=True)
    
    def save(self, *args, **kwargs):
        self.registration_number = "".join(random.choices(string.digits,k=8))
        super(UserProfile, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    def get_full_name(self):
        return "{} {}".format(self.first_name,self.last_name)
    
    @property
    def is_staff(self):
        return self.user.is_staff
    
    @property
    def is_superuser(self):
        return self.user.is_superuser



class Profile(models.Model):
    intern = models.OneToOneField(UserProfile, related_name='profile', on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=64)
    is_active = models.BooleanField(default=False)


class PersonalDetail(models.Model):
    intern = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    phoneNumber = models.CharField(max_length=12)
    whatsapp_no = models.CharField(max_length=12)
    project = models.CharField(max_length=15, choices = PROJECT_CHOICE)
    profile = models.CharField(max_length=12, choices = PROFILE_CHOICE)
    typeofInternship = models.CharField(max_length=15, choices = TYPE_OF_INTERNSHIP)
    joiningDate = models.DateField(auto_now_add=True)
    panNumber = models.CharField(max_length=10)
    aadharNumber = models.CharField(max_length=12)
    emergencyContactNumber = models.CharField(max_length=12)
    bankAccountNumber = models.CharField(max_length=15)
    ifscCode = models.CharField(max_length=10)
    dob = models.DateField()
    permanentAddress = models.TextField()
    currentAddress = models.TextField()
    biometricIdNumber = models.CharField(max_length = 15)
    intership_tenure = models.CharField(max_length=10, choices = TENURE_CHOICE)
    resume = models.FileField(upload_to='resume')


class Project(models.Model):
    profile = models.CharField(max_length=2, choices=PROFILE, default='FR')
    projectWorked = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=1, choices=STATUS,)
    tenure = models.CharField(max_length=3)
    joiningDate = models.DateField()
    endDate = models.DateField()
    uploadTrakerLink = models.URLField()
    mentorLeader = models.TextField()


class Report(models.Model):
    projectName = models.CharField(max_length=100)
    upload_report = models.FileField(upload_to='files')
    status = models.CharField(choices=PROJECT_STATUS, max_length=2,)



from .functions import generate_token, send_email, delete_user_inactive, delete_inactive
# import threading 


@receiver(post_save, sender=UserProfile)
def save_profile(sender, instance,created, **kwargs):
    # delete_inactive(instance.email)
    if created:
        Profile.objects.create(intern=instance, activation_key=generate_token())
        id = instance.user.id
        full_name = instance.first_name + ' ' + instance.last_name
        send_email(full_name, id, instance.user.email)
    pass

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance,created, **kwargs):
    # delete_inactive(instance.email)
    if created:
        if instance.is_superuser:
            UserProfile.objects.create(user=instance, first_name='super', last_name='user')
            intern = UserProfile.objects.all().filter(user=instance).first()
            Profile.objects.create(intern=intern, activation_key=generate_token())
            id = intern.user.id
            full_name = intern.first_name + ' ' + intern.last_name
            send_email(full_name, id, intern.user.email)
            print('Please check your mail to verify email')
    pass



# @receiver(pre_save, sender=User)
# def my_handler(sender, **kwargs):
#     delete_inactive(sender.email)
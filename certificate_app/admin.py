from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ProjectWorkedChoice)
admin.site.register(ProfileChoice)
admin.site.register(StatusChoice)
admin.site.register(TypeOfInternChoice)
admin.site.register(TenureChoice)

admin.site.register(UserProfile)
admin.site.register(Profile)
admin.site.register(Certificate)
admin.site.register(PersonalDetail)
admin.site.register(Project)
admin.site.register(Report)


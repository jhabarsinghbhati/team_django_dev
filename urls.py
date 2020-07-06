from django.contrib import admin
from django.contrib.auth import views as authviews
from django.urls import path,include
from django.conf.urls import url
from irscuser import views
from django.views.generic.base import RedirectView
import home,isafe,drivingtest
from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('setses',views.setsession,name='setses'),
    path('social_login',views.social_login,name='social_login'),
    path('', include('home.urls')),
    path('cityprogram/', include('cityhead.urls')),
    path('isafe/', include('isafe.urls')),
    path('ICSM20/', include('ICSM19.urls')),
    path('morthportal/', include('morthportal.urls')),

    url('hackathon/', include('hackhome.urls')),
    # path('accounts/login/', authviews.LoginView.as_view(), name='myloginn'),
    url(r'^account/', include('social_django.urls', namespace='social')),
    path('socialnew/',views.socialnew ,name="socialnew"),
    path('driving/',views.drivingtest ,name="driving"),# for social login
    path('policy-portal/',include('policyportal.urls')),# for social login
    path('news-portal/',include('newsportal.urls')),
    path('policy-portal2020/',include('policyportal2020.urls')),# for social login
    
    path('intern/',  include('certificate_app.urls'))
    # url(r'^.*$', RedirectView.as_view(url='home/', permanent=False), name='index')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^drivingtest/', include('drivingtest.urls')),
)

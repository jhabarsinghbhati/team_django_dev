from django.urls import path,include,re_path
from .views import reportview,reportupdate,adminpage,create_certificate,change_status,personaldetail,project,\
    register_user,login,confirm_logout_user,register_activation,register_token,forgot_password,forgot_password_confirm,\
        projectupdate,personaldetailupdate
from django.conf.urls import url


app_name = 'certificate_app'

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login, name='login'),
    # path('login-admin/', login_admin, name='admin_login'),
    # path('logout/', logout_user, name='logout'),
    path('logout/', confirm_logout_user, name='confirm_logout'),
    # path('certificate/', intern_certificate, name='intern_certificate'),
    path('register-activation/',register_activation, name='register_activation'),
    re_path(r'register-token/(?P<key>\w{64})/',register_token, name='register_token'),
    path('forgot-password/', forgot_password, name='forgot_password'),
    re_path(r'forgot-password-token/(?P<key>\w{64})/',forgot_password_confirm, name='forgot_password_confirm'),
    # path('personal-details/', views.personal_details, name='personal_details'),
    # path('project-details/', views.project_details, name='project_details'),
    # path('report-submission/', views.report_submission, name='report_submission'),
    # path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin-dashboard/iframe', views.admin_iframe, name='admin_iframe'),


    # url(r'^register',login,name='login'),
    path('personaldetail',personaldetail,name='personal_detail'),
    path('personaldetail/update',personaldetailupdate,name='personal_detail_update'),

    path('project',project,name="project"),
    path('project/update',projectupdate,name="projectupdate"),

    path('report',reportview,name='report'),
    path('report/update',reportupdate,name='reportupdate'),

    path('mentor',adminpage,name='mentor'),
    path('mentor/generate-certficate/<pk>',create_certificate,name='create_certificate'),
    path('mentor/change-status/<int:pk>',change_status,name='change_status'),
]


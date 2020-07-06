from django.urls import path, re_path
from certificate_app import views

app_name = 'certificate_app'

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login, name='login'),
    # path('login-admin/', views.login_admin, name='admin_login'),
    # path('logout/', views.logout_user, name='logout'),
    path('logout/', views.confirm_logout_user, name='confirm_logout'),
    path('certificate/', views.intern_certificate, name='intern_certificate'),
    path('register-activation/',views.register_activation, name='register_activation'),
    re_path(r'register-token/(?P<key>\w{64})/',views.register_token, name='register_token'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    re_path(r'forgot-password-token/(?P<key>\w{64})/',views.forgot_password_confirm, name='forgot_password_confirm'),
    path('personal-details/', views.personal_details, name='personal_details'),
    path('project-details/', views.project_details, name='project_details'),
    path('report-submission/', views.report_submission, name='report_submission'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/iframe', views.admin_iframe, name='admin_iframe'),
]	

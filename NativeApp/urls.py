from django.urls import path
from . import views
from .views import EmployerUpdate, WorkerUpdate, home, user_login,employer_reg,worker_reg,set_availability,PasswordChange,PasswordChangeEmp,AboutUs,ResetPass
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('base/',views.base,name='base'),
    path('',home.as_view(), name='home'),
    # path('employer/', views.Employerlist, name='EmployerList'),
    path('login/', user_login.as_view(), name='user_login'),
    # path('nav/',views.nav,name='nav'),
    path('jobtype/',views.jobtype, name='jobtype'),
    path('employer_reg/', employer_reg.as_view(), name='employer_reg'),
    # path('wb/<str:user_name>/', views.w_base, name='w_base'),
    # path('e_home/<str:user_name>/', views.e_home, name='e_home'),
    # path('ae/',views.admin_emp , name='admin_emp'),
    path('worker_reg/', worker_reg.as_view() , name='worker_reg'),
    path('employer_hire/<int:worker_id>/', views.employer_hire, name='employer_hire'),
    path('negotiate/<int:worker_id>/', views.negotiate, name='negotiate'),
    path('accept_hiring/<int:hiring_id>/',views.accept_hiring, name='accept_hiring'),
    path('reject_hiring/<int:hiring_id>/', views.reject_hiring, name='reject_hiring'),
    path('logout',views.logout, name='logout'),
    path('employer_home/',views.employer_home, name='employer_home'),
    path('worker_home/', views.worker_home, name='worker_home'),
    path('set-availability/', set_availability.as_view(), name='set_availability'),
    path('worker_update/<int:update_id>/', WorkerUpdate.as_view(), name='worker_update'),
    path('employer_update/<int:update_id>/', EmployerUpdate.as_view(), name='employer_update'),
    path('password_change', PasswordChange.as_view(), name="password_change"),
    path('password_change_emp', PasswordChangeEmp.as_view(), name="password_change_emp"),
    path('about_us/', AboutUs.as_view(),name='about_us'),
    path('reset_pass/', ResetPass.as_view(), name='reset_pass')
]

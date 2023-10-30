from django.urls import path
from . import views
from .views import user_login,employer_reg,worker_reg,set_availability


urlpatterns = [
    path('base/',views.base,name='base'),
    path('',views.home, name='home'),
    # path('employer/', views.Employerlist, name='EmployerList'),
    path('login/', user_login.as_view(), name='user_login'),
    path('nav/',views.nav,name='nav'),
    path('type/',views.type, name='type'),
    path('employer_reg/', employer_reg.as_view(), name='employer_reg'),
    # path('wb/<str:user_name>/', views.w_base, name='w_base'),
    # path('e_home/<str:user_name>/', views.e_home, name='e_home'),
    # path('ae/',views.admin_emp , name='admin_emp'),
    path('worker_reg/', worker_reg.as_view() , name='worker_reg'),
    path('employer_hire/<int:worker_id>/', views.employer_hire, name='employer_hire'),
    path('negotiate/<int:worker_id>/', views.negotiate, name='negotiate'),
    path('accept_hiring/<int:hiring_id>/', views.accept_hiring, name='accept_hiring'),
    path('reject_hiring/<int:hiring_id>/', views.reject_hiring, name='reject_hiring'),
    path('logout_worker/',views.logout_worker, name='logout_worker'),
    path('logout_employer/',views.logout_employer, name='logout_employer'),
    path('employer_home/', views.employer_home, name='employer_home'),
    path('worker_home/', views.worker_home, name='worker_home'),
    path('set-availability/', set_availability.as_view(), name='set_availability'),


]

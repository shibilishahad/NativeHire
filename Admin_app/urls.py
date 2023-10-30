from django.urls import path
from .views import *

app_name = 'Admin_app'

urlpatterns = [
    path('', AdminHome.as_view(), name='admin_home'),
    path('admin_emp/', AdminEmp.as_view(), name='admin_emp'),
    path('admin_worker/', AdminWorker.as_view(), name='admin_worker'),
    path('TypeView/', Type.as_view(), name='TypeView'),
    path('delete_employer/', DeleteEmployer.as_view(), name='delete_employer'),
    path('logout_admin/', LogoutAdmin.as_view(), name='logout_admin'),
    path('delete_emp/<int:user_id>/', DeleteEmp.as_view(), name='delete_emp'),
    path('delete_worker/', DeleteWorker.as_view(), name='delete_worker'),
    path('delete_work/<int:user_id>/', DeleteWork.as_view(), name='delete_work'),
]

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from NativeApp.models import Customer,Worker




class CustomerAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['user', 'phone_no', 'location', 'user_type']
    list_per_page = 20
    search_fields = ('user__username', 'phone_no', 'location', 'user_type')
admin.site.register(Customer,CustomerAdmin)

class WorkerAdmin(admin.ModelAdmin):
    list_display = ['user','availability','wage','experience','country','city','job_types']
    list_per_page = 20
admin.site.register(Worker,WorkerAdmin)


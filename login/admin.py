from django.contrib import admin
from home.models import Applicant, Company, Job, Application

admin.site.register(Applicant)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
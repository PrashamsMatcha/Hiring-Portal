from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('welcome', views.home2, name = 'home2'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('updateprofile', views.profile_update_page, name = "updateprofile"),
    path('updateprofilesubmit', views.profile_update_submit, name = "updateprofilesubmit"),
    path('jobdetails/<int:myid>', views.job_details, name = 'job'),
    path('welcome_company', views.home3, name='home3'),
    path('updateprofilesubmit_company', views.profile_update_submit_company, name = "updateprofile_company"),
    path('add_job_page', views.add_job_page, name='add_job_page'),
    path('add_job_submit', views.add_job_submit, name = 'add_job_submit'),
    path('job_list', views.job_list, name='job_list'),
    path('all_applicants', views.all_applicants, name='all_applicants'),
    path('edit_job/<int:myid>', views.edit_job_page, name='edit_job_page'),
    path('edit_job_submit/<int:myid>', views.edit_job_submit, name='edit_job_submit'),
    path('job_apply/<int:myid>', views.job_apply, name="job_apply"),
    path('job_delete_company/<int:myid>', views.job_delete, name ="job_delete_company"),
    path('status_change/<int:myid>/<str:status>', views.status_change, name="status_change")
]
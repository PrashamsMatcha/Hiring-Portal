from django.db import models
from django.contrib.auth.models import User


# Extending User Model Using a One-To-One Link
class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contact = models.IntegerField(null=True,blank=True)
    department = models.CharField(max_length=30, null=True, blank=True)
    college = models.CharField(max_length=50, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    degree = models.CharField(null=True, blank=True, max_length=20)
    current_year = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    update_status = models.CharField(max_length=15)

    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pics')
    docfile = models.FileField(null=True, blank=True, upload_to='resume')

    def __str__(self):
        return self.user.first_name+" "+self.user.last_name
 
class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    image = models.ImageField(upload_to="company_logo")
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)
 
    def __str__ (self):
        return self.company_name
 
class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    deadline = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    image = models.ImageField()
    eligibility = models.TextField(max_length = 400)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField()
    job_profile = models.CharField(max_length=50)
 
    def __str__ (self):
        return self.title
 
class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='applied_resume')
    apply_date = models.DateField()
    status = models.CharField(max_length=30)
 
    def __str__ (self):
        return str(self.applicant)
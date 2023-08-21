from email.mime import application
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Applicant, Application, Job, Company
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
import os

# Create your views here.
def home(request):
    return render(request, 'home/home.html')

def job_details(request, myid):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    company = job.company
    try:
        application = Application.objects.get(applicant = applicant, job = job,company = company)
        return render(request, 'jobs/job_details.html', {'applicant': applicant, 'job': job, 'status':"Applied"})
    except ObjectDoesNotExist:
        application = None
    if application == None:
        return render(request, 'jobs/job_details.html', {'applicant': applicant, 'job': job, 'status': "Not Applied"})
    return render(request, 'jobs/job_details.html', {'applicant': applicant, 'job': job, 'status': "Applied"})

def home2(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    jobs = Job.objects.all().order_by('-start_date')
    today = date.today()
    count = jobs.count()
    number = int(count/3)
    rem = count%3
    data = []
    for i in range(number):
        temp = [jobs[i*3], jobs[i*3+1], jobs[i*3+2]]
        data.append(temp)
    if rem!=0:
        temp = []
        for i in range(1,rem+1):
            temp.append(jobs[number*3+i-1])
        data.append(temp)

    return render(request, 'login/available_internships.html', {'applicant': applicant, 'jobs':jobs, 'data':data})

def home3(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    return render(request, 'company/company_homepage.html', {'company': company})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    return render(request, 'login/updateprofile.html',{'applicant': applicant})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    jobs = Job.objects.all().order_by('-start_date')
    apply = Application.objects.filter(applicant=applicant)
    print(apply)
    data = []
    for i in apply:
        data.append(i.job.id)
    return render(request, 'login/dashboard.html', {'applicant':applicant, 'jobs':jobs, 'data':data, 'apply':apply})

def profile_update_submit(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    if applicant.update_status=="No":
        if request.method=="POST":   
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            college=request.POST['college']
            department=request.POST['department']
            current_year=request.POST['current_year']
            degree=request.POST['degree']
            dob=request.POST['dob']
            contact = request.POST['contact']
        
            profile_pic = request.FILES['profile_pic']
            ext = profile_pic.name.split('.')[-1]
            new_name = first_name+'_'+last_name+'_'+'.'+ext
            profile_pic.name = new_name

            docfile = request.FILES['docfile']
            ext = docfile.name.split('.')[-1]
            new_name = first_name+'_'+last_name+'_'+'.'+ext
            docfile.name= new_name
 
            applicant.user.first_name = first_name
            applicant.user.last_name = last_name
            applicant.contact = contact
            applicant.degree = degree
            applicant.department = department
            applicant.college = college
            applicant.current_year = current_year
            applicant.dob = dob
            applicant.update_status = 'Yes'
            applicant.save()
            applicant.user.save()
            messages.success(request, "Successfully Saved Text Data")

            try:
                applicant.profile_pic = profile_pic
                applicant.docfile = docfile
                applicant.save()
                messages.success(request, "Successfully Saved the Resume and Profile Picture")
            except:
                pass
                messages.error(request, "Could Not Save Profile Picture and Resume. Try Again! ")
            return redirect('updateprofile')
        return redirect('home2')
    else:
        if request.method=="POST":   
            first_name=request.POST['first_name']
            last_name=request.POST['last_name']
            college=request.POST['college']
            department=request.POST['department']
            current_year=request.POST['current_year']
            degree=request.POST['degree']
            contact = request.POST['contact']

            if(request.FILES['profile_pic']!=None):
                profile_pic = request.FILES['profile_pic']
                ext = profile_pic.name.split('.')[-1]
                new_name = first_name+'_'+last_name+'_'+'.'+ext
                profile_pic.name = new_name
                applicant.profile_pic = profile_pic

            if(request.FILES['docfile']!=None):
                docfile = request.FILES['docfile']
                ext = docfile.name.split('.')[-1]
                new_name = first_name+'_'+last_name+'_'+'.'+ext
                docfile.name= new_name
                print(docfile)
                applicant.docfile = docfile

            if(request.POST['dob']!=""):
                dob=request.POST['dob']
                applicant.dob = dob            

            applicant.user.first_name = first_name
            applicant.user.last_name = last_name
            applicant.contact = contact
            applicant.degree = degree
            applicant.department = department
            applicant.college = college
            applicant.current_year = current_year
            applicant.update_status = 'Yes'
            applicant.save()
            applicant.user.save()
            messages.success(request, "Successfully Saved Text Data")

            return redirect('updateprofile')
        return redirect('home2')


def profile_update_page(request):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    
    return render(request, "login/updateprofile.html", {'applicant':applicant})

def profile_update_submit_company(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    if request.method=="POST":   
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        contact = request.POST['contact']
        
        company.user.first_name = first_name
        company.user.last_name = last_name
        company.contact = contact
        company.save()
        company.user.save()

        messages.success(request, "Successfully Saved Data")
        return redirect('home3')
    return redirect('home3')

def add_job_page(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    return render(request, 'company/add_job_page.html', {'company':company})

def add_job_submit(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        image = company.image.url
        eligibility = request.POST['eligibility']
        location = request.POST['location']
        skills = request.POST['skills']
        deadline = request.POST['deadline']
        job_profile = request.POST['job_profile']
        description = request.POST['description']

        if(deadline>start_date or deadline>end_date):
            messages.error(request, "Please Choose Appropriate Dates!")
            return redirect('add_job_page')
        if(start_date>end_date):
            messages.error(request, "Please Choose Appropriate Dates!")
            return redirect('add_job_page')
        job = Job.objects.create(company=company, title=title,start_date=start_date, end_date=end_date, salary=salary, image=image, eligibility=eligibility, location=location, skills=skills, description=description, creation_date=date.today(), deadline = deadline, job_profile=job_profile)
        job.save()
        messages.success(request, "Successfully Added the Internship!")
        return redirect('add_job_page')
    return redirect('add_job_page')

def job_list(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    jobs = Job.objects.filter(company=company) 
    return render(request, "company/job_list.html", {'jobs':jobs, 'company': company})

def all_applicants(request):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    application = Application.objects.filter(company=company).order_by('job')
    jobs = Job.objects.filter(company=company)
    print(application)
    return render(request, "company/all_applicants.html", {'application':application, 'company': company, 'jobs':jobs})

def edit_job_page(request, myid):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    company = Company.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    return render(request, 'company/edit_job.html', {'company':company, 'job':job})

def edit_job_submit(request, myid):
    if not request.user.is_authenticated:
        return redirect('company_signin')
    job = Job.objects.get(id=myid)
    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        eligibility = request.POST['eligibility']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']
        job_profile = request.POST['job_profile']
        deadline = request.POST['deadline']

        job.title = title
        job.salary = salary
        job.eligibility = eligibility
        job.location = location
        job.skills = skills
        job.job_profile = job_profile
        job.description = description
        job.save()

        if start_date:
            job.start_date = start_date
            job.save()
        if end_date:
            job.end_date = end_date
            job.save()
        if deadline:
            job.deadline = deadline
            job.save()

        messages.success(request, "Job Details Successfully Updated! ")
        return redirect('job_list')
    return redirect('job_list')

def job_apply(request, myid):
    if not request.user.is_authenticated:
        return redirect('signin')
    applicant = Applicant.objects.get(user=request.user)
    if(applicant.update_status == "No"):
        messages.error(request, "Please Complete Your Profile!")
        return redirect('home2')
    job = Job.objects.get(id=myid)
    date1 = date.today()
    if job.deadline < date1:
        messages.error(request, "Error! Could Not Apply Since Internship's Deadline Has Passed")
        return redirect('home2')
    else:
        if request.method == "POST":
            resume = applicant.docfile
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume, apply_date=date.today(), status="Applied")
            messages.success(request, "Successfully Applied To " + job.title + " - " + job.company.company_name)
            return redirect("home2")
    return redirect("home2")

def job_delete(request, myid):
    if not request.user.is_authenticated:
        return redirect("login")
    job = Job.objects.get(id = myid)
    job.delete()
    messages.success(request, "Successfully Deleted the Internship Post")
    return redirect('job_list')

def status_change(request, myid, status):
    if not request.user.is_authenticated:
        return redirect("login")
    application = Application.objects.get(id=myid)
    if(status=="shortlisted"):
        application.status="Shortlisted"
    elif(status=="under_process"):
        application.status="Processing"
    elif(status=="rejected"):
        application.status="Rejected"
    else:
        application.status="Selected"
    application.save()
    return redirect('all_applicants')




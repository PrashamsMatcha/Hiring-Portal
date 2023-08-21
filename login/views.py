from http.client import HTTPResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import Applicant, Company

# Create your views here.
def choice(request):
    return render(request, 'login/login.html')

def signin(request):
    return render(request, 'login/signin.html')

def student(request):
    return render(request, 'login/student_signup.html')

def recruiter(request):
    return render(request, 'login/recruiter_signup.html')

def companysignin(request):
    return render(request, 'login/companysignin.html')

def student_handleSignUp(request):
    if request.method == 'POST':

        #Get the post parameters
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        username = request.POST['email']
        pass1= request.POST['pass1']
        pass2 = request.POST['pass2']
        gender = request.POST['gender']

        #check for erronous inputs
        if(pass1 != pass2):
            messages.error(request, "Passwords do not match")
            return redirect('student_signup')

        if(not first_name.isalnum()):
            messages.error(request, "Name should only be AlphaNumeric")
            return redirect('student_signup')

        if(not last_name.isalnum()):
            messages.error(request, "Name should only be AlphaNumeric")
            return redirect('student_signup')

        #create the user
        myuser = User.objects.create_user(first_name=first_name, last_name=last_name, username=username, password=pass1)
        applicant = Applicant.objects.create(user=myuser, gender=gender, type="applicant", update_status= 'No')
        myuser.save()
        applicant.save()
        messages.success(request, "Your account has been successfully created.")

        return redirect('signin')
    else:
        return redirect('student_signup')

def student_handleLogin(request):
    if request.user.is_authenticated:
        return redirect("home2")
    else:
        if request.method=="POST":
            loginusername = request.POST['loginusername']
            loginpass = request.POST['loginpass']

            user = authenticate(username = loginusername, password = loginpass)
            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user.is_superuser:
                    login(request, user)
                    messages.success(request, "Admin Logged IN")
                    return redirect("/all_companies")
                elif user1.type == "applicant":
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return redirect('home2')
                else:
                    messages.error(request, "Invalid Credentials, Please Try Again")
                    return redirect('signin')
            
            

    return HTTPResponse('404 - Not Found')

def company_handleSignUp(request):
    if request.method == 'POST':

        #Get the post parameters
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        phone = request.POST['contact']
        image = request.FILES['image']
        company_name = request.POST['company']

        #check for erronous inputs
        if(pass1 != pass2):
            messages.error(request, "Passwords do not match")
            return redirect('recruiter_signup')

        if(not first_name.isalnum()):
            messages.error(request, "Name should only be AlphaNumeric")
            return redirect('recruiter_signup')

        if(not last_name.isalnum()):
            messages.error(request, "Name should only be AlphaNumeric")
            return redirect('recruiter_signup')
        if(len(phone)!=10):
            messages.error(request, "Phone Number should Be 10 Digits Long")
            return redirect('recruiter_signup')

        #create the user
        try:
            user = User.objects.create_user(first_name=first_name, last_name=last_name, username=email, password=pass1)
            company = Company.objects.create(user=user, phone=phone, image=image, company_name=company_name, type="company", status="accepted")
            user.save()
            company.save()
            messages.success(request, "Your account has been successfully created.")
        except:
            messages.error("Sign Up Failed! An Account With Same Credentials Exists")        

        return redirect('company_signin')
    else:
        return redirect('companysignup')

def student_handleLogin(request):
    if request.user.is_authenticated:
        return redirect("home2")
    else:
        if request.method=="POST":
            loginusername = request.POST['loginusername']
            loginpass = request.POST['loginpass']

            user = authenticate(username = loginusername, password = loginpass)
            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return redirect('home2')
                else:
                    messages.error(request, "Invalid Credentials, Please Try Again")
                    return redirect('signin')
    return HTTPResponse('404 - Not Found')
    
def company_handleLogin(request):
    if request.user.is_authenticated:
        return redirect("home3")
    else:
        if request.method=="POST":
            loginusername = request.POST['loginusername']
            loginpass = request.POST['loginpass']
            user = authenticate(username = loginusername, password = loginpass) 

            if user is not None:
                user1 = Company.objects.get(user=user)
                if user1.type == "company" and user1.status != "pending":
                    login(request, user)
                    messages.success(request, "Successfully Logged In")
                    return redirect("home3")
                else:
                    messages.error(request, "Invalid Credentials or Your Status is still Pending. Please Try Again")
                    return redirect('company_signin')
        return HTTPResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully Logged Out")
    return redirect('login')

    
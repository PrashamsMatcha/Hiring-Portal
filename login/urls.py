from django.urls import path
from login import views

urlpatterns = [
    path('', views.choice, name="login"),
    path('student',views.student, name="student_signup" ),
    path('recruiter',views.recruiter, name="recruiter_signup" ),
    path('companysignup', views.company_handleSignUp, name = "companysignup"),
    path('signup', views.student_handleSignUp, name = "handlesignup"),
    path('signin',views.signin, name="signin" ),
    path('companysignin',views.companysignin, name="company_signin" ),
    path('companysigningin',views.company_handleLogin, name="company_handleLogin" ),
    path('signingin', views.student_handleLogin, name = "handleLogin"),
    path('signout', views.handleLogout, name = "handleLogout")
]
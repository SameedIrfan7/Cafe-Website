from django.shortcuts import render, redirect
from uuid import uuid4
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.mail import send_mail
from random import randint
from django.conf import settings
from customer.models import Customer



  # Adjust this import based on your project structure


def home(request):
    return render(request,'index.html')

def about_view(request):
    return render(request,'about.html')

def contact_view(request):
    return render(request,'contact.html')

def index_view(request):
    return redirect(request,'index.html')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        #check the email & password
        # start the session
        try:
            session_user = Customer.objects.get(email = request.POST['email'])
            # validating password
            if request.POST['password'] == session_user.password:
                #starting the session
                request.session['email'] = session_user.email
                return redirect('home')

            else:
                return render(request, 'login.html', {'msg': "Invalid Password!!"})
        except:
            # if entered email is not registered
            return render(request, 'login.html', {"msg":'This email is not registered'})
        return redirect(request,'register,html')



    
def menu_view(request):
    return render(request,'menu.html')

def register_view(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # email validation
        form_email = request.POST['email']
        try:
            #checking if email entered in html form is present inside db
            user_obj = Customer.objects.get(email = form_email)
            return render(request, 'register.html', {'msg': 'This email is already in Use.'})

        except:
            # error occurred while finding that email in DB
            # it means entered email is completely new
            # we can create a new account for it..


            # password & confirm password validation
            if request.POST['password'] == request.POST['cpassword']:
                global c_otp
                c_otp = randint(100_000, 999_999)
                global user_data
                user_data = {
                    'full_name': request.POST['full_name'],
                    'email': request.POST['email'],
                    'password':request.POST['password'],
                    'mobile': request.POST['mobile'],
                    'address': request.POST['address'],
                    'cpassword': request.POST['cpassword']
                }

                subject = 'Cafe Website Registration'
                message = f'Hello!! your OTP is {c_otp}'
                sender = settings.EMAIL_HOST_USER
                rec = [request.POST['email']]
                send_mail(subject, message, sender, rec)
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html', {'msg': 'BOTH passwords do not matchh!!!'})

def single_view(request):
    return render(request,'single.html')





    

# Create your views here.

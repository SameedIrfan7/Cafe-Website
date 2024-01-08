<<<<<<< HEAD
from django.shortcuts import render, redirect
from customer.models import Customer
from random import randint
from django.conf import settings
from django.core.mail import send_mail



# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')
        
def single(request):
    return render(request, 'single.html')

def contact(request):
    return render(request, 'contact.html')

def header(request):
    return render(request, "header.html")

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # email validation
        form_email = request.POST['email']
        try:
            #checking if email entered in html form is present inside db
            user_obj = Customer.objects.get(email = form_email)
            return render(request, 'register.html', {'msg': 'This email is already in Use'})
        
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

                subject = "Your Unique Code to Sweeten Your Next Order at Halal-Cafe's"
                message = f'Hello your OTP is {c_otp}'
                sender = settings.EMAIL_HOST_USER
                rec = [request.POST['email']]
                send_mail(subject, message, sender, rec)
                return render(request, 'otp.html')
            else:
                return render(request, 'register.html', {'msg': 'BOTH passwords do not matchh!!!'})
 
def otp(request):
    pass
    # compare otp entered by user and generated otp
    # c_otp = 315308 INTEGER
    # request.POST['u_otp'] = '315308' STRING

    if str(c_otp) == request.POST['u_otp']:
        # create a row in db
        Customer.objects.create(
            full_name = user_data['full_name'],
            email = user_data['email'],
            password = user_data['password'],
            address = user_data['address'],
            mobile = user_data['mobile']
        )
        
        return render(request, 'register.html', {'msg': 'Account Created Successfully!!!'})

    else:
        return render(request, 'otp.html', {'msg': "entered OTP is INVALID"})
    
def login(request):
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
                return redirect('index')

            else:
                return render(request, 'login.html', {'msg': "Invalid Password!!"})
        except:
            # if entered email is not registered
            return render(request, 'login.html', {"msg":'This email is not registered'})
        
=======
from django.shortcuts import render

# Create your views here.
>>>>>>> 7bd1ddb8542b68a91eb1d655f7d91b32ca367ab7

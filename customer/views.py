from django.shortcuts import render, redirect
from customer.models import Customer, Cart, Orders
from seller.models import Product
from random import randint
from django.conf import settings
from django.core.mail import send_mail
import razorpay
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from uuid import uuid4



razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

# Create your views here.
def home(request):
    if 'email' in request.session:
        user_obj=Customer.objects.get(email=request.session['email'])
        return render(request, 'index.html',{'user_data':user_obj})
    else:
        return render(request, 'index.html')



def about(request):
    if 'email' in request.session:
        user_obj=Customer.objects.get(email=request.session['email'])
        return render(request, 'about.html', {'user_data':user_obj})
    else:
        return render(request, 'about.html')


def menu(request):
    all_products = Product.objects.all()
    if 'email' in request.session:
        user_obj=Customer.objects.get(email=request.session['email'])
        return render(request, 'menu.html',{'user_data':user_obj, 'all_products':all_products})
    else:
        return render(request, 'menu.html', {'all_products':all_products})

        
def single(request):
    if 'email' in request.session:
        user_obj=Customer.objects.get(email=request.session['email'])
        return render(request, 'single.html', {'user_data':user_obj})
    else:
        return render(request, 'single.html')


def contact(request):
    if 'email' in request.session:
        user_obj=Customer.objects.get(email=request.session['email'])
        return render(request, 'contact.html', {'user_data':user_obj})
    else:
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
                return redirect('home')

            else:
                return render(request, 'login.html', {'msg': "Invalid Password!!"})
        except:
        #     # if entered email is not registered
              return render(request, 'login.html', {"msg":'This email is not registered'})
    
    
    
    
def logout(request):
    del request.session['email']
    return redirect('home') # name= argument in urls.py



def add_to_cart(request, pk):
    if 'email' in request.session:
        #add that product in db table
        Cart.objects.create(
            buyer = Customer.objects.get(email= request.session['email']),
            product = Product.objects.get(id = pk)
        )
        return redirect('menu')
    else:
        # no buyer has logged in
        return redirect('login')
    
    
    
    
def cart(request):
    try:
        user_data = Customer.objects.get(email = request.session['email'])
        my_cart = Cart.objects.filter(buyer = user_data)
        p_count = len(my_cart)
        total_cost = 0

        if p_count == 0:
            return render(request, 'cart.html', {'user_data':user_data,'msg':"Your cart is empty",'p_count':p_count, 'total_cost':total_cost})

        for i in my_cart:
            total_cost += i.product.price
        
        context = {
        'user_data':user_data,
        'my_cart':my_cart,
        'p_count':p_count, 
        'total_cost':total_cost
        }

        # payment portion
        global amount
        amount = total_cost * 100 #paise version
        currency = 'INR'
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                       currency=currency,
                                                       payment_capture='0'))
        razorpay_order_id = razorpay_order['id']
        callback_url = 'paymenthandler/'

        #updating context dictionary
        context['razorpay_order_id'] = razorpay_order_id
        context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
        context['razorpay_amount'] = amount
        context['currency'] = currency
        context['callback_url'] = callback_url

        return render(request, 'cart.html', context=context)
    except:
        return redirect('login')




@csrf_exempt
def paymenthandler(request):

    # only accept POST request.
    if request.method == "POST":
        try:
           
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is not None:
                f_amount = amount  # Rs version 
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, f_amount)

                    user_data = Customer.objects.get(email = request.session['email'])
                    cart_items = Cart.objects.filter(buyer = user_data)
                    for item in cart_items:

                        #reduce product stock
                        pro = Product.objects.get(id = item.product.id)
                        pro.stock -= 1
                        pro.save()

                        #creating order for that item
                        Orders.objects.create(
                            order_id = uuid4(),
                            product = pro,
                            buyer = user_data,
                            status = 'Order Placed',
                            payment_id = payment_id
                        )

                        #deleting that Item from Cart
                        item.delete()

                    # render success page on successful caputre of payment
                    return render(request, 'paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
    
    
    
    
def del_cart(req,pk):
    c1 = Cart.objects.get(id = pk)
    c1.delete()
    return redirect('cart')
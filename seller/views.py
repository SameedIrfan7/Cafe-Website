from django.shortcuts import render, redirect
from seller.models import SellerTable, CategoryTable, Product
from customer.models import Orders
from random import randint
from django.conf import settings
from django.core.mail import send_mail
# Create your views here.


# this decorator is for validating login
def login_needed(fun1):
    def inner_fun(request):
        if 'seller_email' not in request.session:
            return redirect('seller_login')
        else:
            return fun1(request)
    return inner_fun


@login_needed
def index_view(request):
    user_data = SellerTable.objects.get(email=request.session['seller_email'])
    order_items = Orders.objects.filter(product__seller = user_data).exclude(status='Delivered')
    return render(request,'seller_index.html', {"user_data":user_data, 'order_items':order_items})
    

def login_view(request):
    if request.method == 'GET':
        return render(request, 'seller_login.html')
    else:
        #check the email & password
        # start the session
        # try:
        session_user = SellerTable.objects.get(email = request.POST['email'])
        # validating password
        if request.POST['password'] == session_user.password:
            #starting the session
            request.session['seller_email'] = session_user.email
            return redirect('seller_index')

        else:
            return render(request, 'seller_login.html', {'msg': "Invalid Password!!"})
    # except:
        # if entered email is not registered
        return render(request, 'seller_login.html', {"msg":'This email is not registered'})

def register_view(request):
    if request.method == 'GET':
        return render(request, 'seller_register.html')
    else:
        # email validation
        form_email = request.POST['email']
        try:
            #checking if email entered in html form is present inside db
            user_obj = SellerTable.objects.get(email = form_email)
            return render(request, 'seller_register.html', {'msg': 'This email is already in Use.'})

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
                    'gst_number': request.POST['gst_number'],
                    'cpassword': request.POST['cpassword']
                }

                subject = 'Ecommerce Seller Registration'
                message = f'Hello!! your OTP is {c_otp}'
                sender = settings.EMAIL_HOST_USER
                rec = [request.POST['email']]
                send_mail(subject, message, sender, rec)
                return render(request, 'seller_otp.html')
            else:
                return render(request, 'seller_register.html', {'msg': 'BOTH passwords do not matchh!!!'})
        
        
def otp_view(request):
    pass
    # compare otp entered by user and generated otp
    # c_otp = 315308 INTEGER
    # request.POST['u_otp'] = '315308' STRING

    if str(c_otp) == request.POST['u_otp']:
        # create a row in db
        SellerTable.objects.create(
            gst_number = user_data['gst_number'],
            seller_name = user_data['full_name'],
            email = user_data['email'],
            password = user_data['password'],
        )
        return render(request, 'seller_register.html', {'msg': 'Account Created Successfully!!!'})

    else:
        return render(request, 'seller_otp.html', {'msg': "entered OTP is INVALID"})


def logout_view(request):
    del request.session['seller_email']
    return redirect('seller_login')

@login_needed
def add_product(request):
    user_data = SellerTable.objects.get(email = request.session['seller_email'])
    all_categories = CategoryTable.objects.all()
    if request.method == 'GET':
        return render(request, 'add_product.html', {'user_data':user_data, 'categories':all_categories})
    else:
        # create a row in Product db table
        
        Product.objects.create(
        product_name = request.POST['product_name'],
        image = request.FILES['image'],
        des = request.POST['des'],
        price = request.POST['price'],
        stock = request.POST['stock'],
        seller = SellerTable.objects.get(email = request.session['seller_email']),
        category= CategoryTable.objects.get(id = int(request.POST['category']))
        )      
        return render(request, 'add_product.html', {'user_data':user_data, 'msg': 'Product Successfully Added!!', 'categories':all_categories})



def inventory_view(request):
    user_data = SellerTable.objects.get(email = request.session['seller_email'])
    my_products = Product.objects.filter(seller = user_data)
    return render(request, 'inventory.html', {'user_data': user_data, 'my_products':my_products})

def edit_product(request, pk):
    product_info = Product.objects.get(id = pk)
    if request.method == 'GET':
        all_c = CategoryTable.objects.all()
        user_data = SellerTable.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'product': product_info, 'categories':all_c, 'user_data':user_data})
    else:
        if request.FILES:
            product_info.image = request.FILES['image']
        product_info.product_name = request.POST['product_name']
        product_info.price = request.POST['price']
        product_info.stock = request.POST['stock']
        product_info.des = request.POST['des']
        product_info.category = CategoryTable.objects.get(id = request.POST['category'])

        product_info.save() # it will update in db
        
        all_c = CategoryTable.objects.all()
        user_data = SellerTable.objects.get(email = request.session['seller_email'])
        return render(request, 'edit_product.html', {'product': product_info, 'categories':all_c, 'user_data':user_data, 'msg':"Successfully Updated!!"})

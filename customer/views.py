from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html')

def about_view(request):
    return render(request,'about.html')


def contact_view(request):
    return render(request,'contact.html')


def index_view(request):
    return render(request,'index.html')


def login_view(request):
    return render(request,'login.html')


def menu_view(request):
    return render(request,'menu.html')


def register_view(request):
    return render(request,'register.html')


def single_view(request):
    return render(request,'single.html')
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def menu(request):
    return render(request, 'menu.html')

def login(request):
    return render(request, 'login.html')

def single(request):
    return render(request, 'single.html')

def contact(request):
    return render(request, 'contact.html')

def register(request):
    return render(request, "register.html")

def header(request):
    return render(request, "header.html")
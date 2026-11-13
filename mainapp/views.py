from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from adminapp.models import *

# Create your views here.
def index(request):
    books=Book.objects.all()
    war_books = Book.objects.filter(category__name='war')
    tech_books = Book.objects.filter(category__name='technology')
    context={
        'books':books,
        'war_books':war_books,
        'tech_books':tech_books,
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")

def register(request):
    if request.method =="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')
        if password!=cpassword:
            messages.warning(request,"password and confirm password do not matched")
            return redirect('register')
        check=Logininfo.objects.filter(username=email)
        # for match password or confirm password
        if check:
            messages.warning(request,"this email is already register")
            return redirect('register')
        log=Logininfo(username=email,password=password)
        user=Usreinfo(login=log,name=name,email=email,contactno=contactno)
        log.save()
        user.save()
        messages.success(request,"Registration successful")
        return redirect('register')
    return render(request,"register.html")

def login(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            user=Logininfo.objects.get(usertype="user",username=username,password=password)
            if user is not None:
                messages.success(request,"welcome user")
                request.session['userid']=user.username
                return redirect('userdash')
        except Logininfo.DoesNotExist:
            messages.error(request,"Invalid credentials")
            return redirect('login')    
    return render(request,'login.html')

def contact(request):
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        contactno=request.POST.get('contactno')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        Enquiry.objects.create(name=name,email=email,contactno=contactno,subject=subject,message=message)
        messages.success(request, "Enquiry is successfully submite")
        return redirect('contact')
    return render(request,'contact.html')

def adminlogin(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        try:
            admin=Logininfo.objects.get(usertype="admin",username=username,password=password)
            if admin is not None:
                messages.success(request,"welcome admin")
                request.session['adminid']=admin.username
                return redirect('admindash')
        except Logininfo.DoesNotExist:
            messages.error(request,"Invalid credentials")
            return redirect('adminlogin')    
    return render(request,'adminlogin.html')

def book_details(request,id):
    book=Book.objects.get(id=id)
    context={
        'book':book,
    }
    return render(request,"book_details.html",context)
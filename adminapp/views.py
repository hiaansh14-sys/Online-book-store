from django.shortcuts import render,redirect
from django.contrib import messages

from mainapp.models import *
from .models import*

# Create your views here.
def admindash(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'admin':adminid
    }
    return render(request,"admindash.html",context)

def adminlogout(request):
    if 'adminid' in request.session:
        del request.session['adminid']
        messages.success(request,"you are logged out")
        return redirect('index')
    else:
        messages.error(request,'something going went wrong')
        return redirect('index')

def addcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'admin':adminid
    }
    if request.method=="POST":
        name=request.POST.get('name')
        description=request.POST.get('description')
        check=Category.objects.create(name=name,description=description)
        if check:
            messages.warning(request,"category already exists")    
            return redirect('addcat')
        Category.objects.create(name=name,description=description)
        messages.success(request,"Category added succussfully,")
        return redirect('addcat')
    return render(request,"addcat.html")

def viewcat(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'admin':adminid
    }
    return render(request,"viewcat.html")

def viewbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'admin':adminid
    }
    return render(request,"viewbook.html")

def addbook(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    categories=Category.objects.all()
    context={
        'admin':adminid,
        'categories':categories
    }
    if request.method=="POST":
        title=request.POST.get('title')
        author=request.POST.get('author')
        catid=request.POST.get('catid')
        cat=Category.objects.get(id=catid)
        description=request.POST.get('description')
        original_price=request.POST.get('original_price')
        price=request.POST.get('price')
        published_date=request.POST.get('published_date')
        language=request.POST.get('language')
        cover_image=request.FILES.get('cover_image')
        stock=request.POST.get('stock')
        Book.objects.create(
            title=title,
            author=author,
            category=cat,
            description=description,
            original_price=original_price,
            price=price,
            published_date=published_date,
            language=language,
            cover_image=cover_image,
            stock=stock
        )
        messages.success(request,"new book added successfully")
        return redirect('addbook')
    return render(request,"addbook.html",context)

def changepassword(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    context={
        'admin':adminid
    }
    return render(request,"changepassword.html")

def enquiries(request):
    if not 'adminid' in request.session:
        messages.error(request,"you are not logged in")
        return redirect('adminlogin')
    adminid=request.session.get('adminid')
    enqs=Enquiry.objects.all()
    context={
        'admin':adminid,
        'enqs':enqs
    }
    return render(request,"enquiries.html",context)


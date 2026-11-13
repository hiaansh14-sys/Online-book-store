from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from mainapp.models import Usreinfo
from adminapp.models import *
from .models import *

# Dashboard
def userdash(request):
    if 'userid' not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)

    # Get cart data
    cart, created = Cart.objects.get_or_create(user=user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_count = cart_items.count()
    cart_total = sum(item.get_total_price() for item in cart_items)

    # Get order data
    orders = Order.objects.filter(user=user).order_by('-ordered_at')
    order_count = orders.count()
    total_spent = sum(order.total_amount for order in orders)

    # Get recent orders (last 5)
    recent_orders = orders[:5]

    context = {
        'userid': userid,
        'user': user,
        'cart_count': cart_count,
        'cart_total': cart_total,
        'order_count': order_count,
        'total_spent': total_spent,
        'recent_orders': recent_orders,
    }
    return render(request, "userdash.html", context)


# Logout
def userlogout(request):
    if 'userid' in request.session:
        del request.session['userid']
        messages.success(request, "You are logged out successfully.")
    else:
        messages.warning(request, "Something went wrong.")

    return redirect('index')


# View Profile
def userprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your profile.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)

    return render(request, "userprofile.html", {'userid': userid, 'user': user})


# Edit Profile
def editprofile(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to edit your profile.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)
    context={
        'userid':userid,
        'user':user
    }
    if request.method =="POST":
        name=request.POST.get('name')
        contactno=request.POST.get('contactno')
        picture=request.FILES.get('profile')
        address=request.POST.get('address')
        user.name=name
        user.contactno=contactno
        if picture:
            user.picture=picture
        user.address=address
        user.save()    
        messages.success(request,"your profile has been updated.")
        return redirect('userprofile')
    return render(request, "editprofile.html",context)


# View Cart
def viewcart(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your cart.")
        return redirect('login')
    userid=request.session.get('userid')
    user=Usreinfo.objects.get(email=userid)
    ucart=Cart.objects.filter(user=user)
    if not ucart:
        Cart.objects.create(user=user)
    cart=Cart.objects.get(user=user)
    items = CartItem.objects.filter(cart=cart)
    total_price = 0
    for i in items:
        total_price+= i.get_total_price()
    context={
        'userid':userid,
        'user':user,
        'items':items,
        'total_price' : total_price
    }  
    return render(request, "viewcart.html",context)


# Orders
def userorders(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to view your orders.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)
    login_user = Logininfo.objects.get(username=userid)

    # Get all orders for this user
    orders = Order.objects.filter(user=user).order_by('-ordered_at')

    # Get order items for each order
    for order in orders:
        order.items = OrderItem.objects.filter(order=order)

    context = {
        'userid': userid,
        'user': user,
        'orders': orders,
    }
    return render(request, "userorders.html", context)


# Change Password
def userpass(request):
    if 'userid' not in request.session:
        messages.error(request, "Please login to change your password.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)
    login_user = Logininfo.objects.get(username=userid)

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Verify current password
        if login_user.password != current_password:
            messages.error(request, "Current password is incorrect.")
            return redirect('userpass')

        # Check if new password and confirm password match
        if new_password != confirm_password:
            messages.error(request, "New password and confirm password do not match.")
            return redirect('userpass')

        # Update password
        login_user.password = new_password
        login_user.save()
        messages.success(request, "Password changed successfully.")
        return redirect('userdash')

    context = {
        'userid': userid,
        'user': user,
    }
    return render(request, "userpass.html", context)

def userbase(request):
    return render(request, 'userbase.html')

def addtocart(request, bid,operator):
    if not 'userid' in request.session:
        messages.error(request, "you are not logged in .")
        return redirect('login')
    userid = request.session.get('userid')
    user = Usreinfo.objects.get(email=userid)
    if request.method == "POST":
        book=Book.objects.get(id=bid)
        quantity = int(request.POST.get('quantity', 1))

        book = Book.objects.get(id=bid)
        cart, created = Cart.objects.get_or_create(user=user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)
        if not item_created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
            cart_item.save()
        messages.success(request, f"Added {quantity} of {book.title} to your cart.")
        return redirect('viewcart')

def removeitem(request,id):
    if not 'userid' in request.session:
        messages.error(request,"You are not logged in.")
        return redirect('login')
    userid= request.session.get('userid')
    user = Usreinfo.objects.get(email=userid)
    ci = CartItem.objects.filter(id=id)
    ci.delete()
    messages.success(request,"Remove item fro cart")
    return redirect('viewcart')

def updateitem(request,id,operator):
    if not 'userid' in request.session:
        messages.error(request, "You are not logged in")
        return redirect('login')
    userid = request.session.get('userid')
    user = Usreinfo.objects.get(email=userid)
    ci = CartItem.objects.get(id=id)
    if operator == '+':
        ci.quantity += 1
        if ci.book.stock < ci.quantity:
            messages.warning(request, "Item quantity is exceeded than stock")
            return redirect('viewcart')
    elif operator == '-':
        ci.quantity -= 1
        if ci.quantity == 0:
            ci.delete()
            messages.warning(request, "Removed")
            return redirect('viewcart')
    ci.save()
    messages.success(request, "Item quantity updated successfully")
    return redirect('viewcart')
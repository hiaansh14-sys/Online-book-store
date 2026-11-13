from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .models import Payment
from userapp.models import Cart, CartItem
from mainapp.models import Usreinfo
from django.contrib import messages

# Create your views here.

def create_payment(request):
    """Create Razorpay order for checkout"""
    if 'userid' not in request.session:
        messages.error(request, "Please login to proceed with payment.")
        return redirect('login')

    userid = request.session['userid']
    user = Usreinfo.objects.get(email=userid)

    # Get user's cart
    try:
        cart = Cart.objects.get(user=user)
        cart_items = CartItem.objects.filter(cart=cart)
        total_amount = sum(item.get_total_price() for item in cart_items)

        if total_amount == 0:
            messages.warning(request, "Your cart is empty.")
            return redirect('viewcart')

        # Convert to paise (Razorpay uses smallest currency unit)
        amount_in_paise = int(total_amount * 100)

        # Create Razorpay order
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order_data = {
            'amount': amount_in_paise,
            'currency': 'INR',
            'receipt': f'receipt_{user.id}',
            'payment_capture': '1'
        }

        razorpay_order = client.order.create(order_data)

        # Save payment record
        payment = Payment.objects.create(
            user=user,
            razorpay_order_id=razorpay_order['id'],
            amount=total_amount,
            currency='INR',
            status='created'
        )

        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount_in_paise,
            'currency': 'INR',
            'user': user,
            'total_amount': total_amount,
            'cart_items': cart_items,
        }

        return render(request, 'payment/checkout.html', context)

    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty.")
        return redirect('viewcart')


@csrf_exempt
def payment_success(request):
    """Handle successful payment"""
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            # Verify signature
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            params = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            client.utility.verify_payment_signature(params)

            # Update payment record
            payment = Payment.objects.get(razorpay_order_id=order_id)
            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = 'paid'
            payment.save()

            # Clear cart after successful payment
            # (You can add order creation logic here later)

            messages.success(request, "Payment successful! Thank you for your purchase.")
            return redirect('userdash')

        except Exception as e:
            messages.error(request, f"Payment verification failed: {e}")
            return redirect('viewcart')

    return redirect('viewcart')


@csrf_exempt
def payment_failure(request):
    """Handle failed payment"""
    messages.error(request, "Payment failed. Please try again.")
    return redirect('viewcart')

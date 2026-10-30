from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Order


@login_required(login_url='login')
def index(request):
    """
    Exclusive catalog view—accessible only to logged-in members.
    """
    try:
        products = Product.objects.all()
    except Exception:
        products = []
        
    return render(request, 'store/index.html', {'products': products})


def register_view(request):
    """
    Handles customer registration.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to NeXora!")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    """
    Handles member login.
    """
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    """
    Logs out current user session.
    """
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def process_checkout(request):
    """
    Processes order creation and emails owner.
    """
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        total = request.POST.get('total', '0.00')

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            shipping_address=address,
            total_amount=total
        )

        subject = f"🚨 New NeXora Order #{order.id}"
        message = (
            f"New order received!\n\n"
            f"Customer: {full_name}\n"
            f"Email: {email}\n"
            f"Phone: {phone}\n"
            f"Total: ${total}\n\n"
            f"Address:\n{address}"
        )
        
        try:
            owner_email = getattr(settings, 'OWNER_EMAIL', settings.DEFAULT_FROM_EMAIL)
            send_mail(
                subject, 
                message, 
                settings.DEFAULT_FROM_EMAIL, 
                [owner_email], 
                fail_silently=True
            )
        except Exception:
            pass

        return render(request, 'store/order_success.html', {'order': order})

    return redirect('index')
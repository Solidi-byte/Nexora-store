from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category


@login_required(login_url='login')
def index(request):
    """
    Exclusive catalog view with category genre filtering.
    """
    category_slug = request.GET.get('category')
    categories = Category.objects.all()
    
    if category_slug:
        products = Product.objects.filter(category__slug=category_slug)
    else:
        products = Product.objects.all()
        
    return render(request, 'store/index.html', {
        'products': products,
        'categories': categories,
        'current_category': category_slug
    })


@login_required(login_url='login')
def product_detail(request, pk):
    """
    Product detail page for color and size selection.
    """
    product = get_object_or_404(Product, pk=pk)
    colors = ['Black', 'White', 'Brown', 'Grey']
    sizes = ['Small (S)', 'Medium (M)', 'Large (L)', 'X-Large (XL)', 'XX-Large (XXL)']
    return render(request, 'store/product_detail.html', {
        'product': product,
        'colors': colors,
        'sizes': sizes
    })


@login_required(login_url='login')
def checkout(request, pk):
    """
    Payment and checkout page with account details and order submission.
    """
    product = get_object_or_404(Product, pk=pk)
    selected_color = request.GET.get('color', 'Black')
    selected_size = request.GET.get('size', 'Medium (M)')

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        # Order processing & confirmation render
        return render(request, 'store/order_success.html', {
            'product': product,
            'color': selected_color,
            'size': selected_size,
            'full_name': full_name
        })

    return render(request, 'store/checkout.html', {
        'product': product,
        'color': selected_color,
        'size': selected_size
    })


def register_view(request):
    """
    Handles customer registration for store access.
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
    Handles member authentication login.
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
    Logs out the current user session.
    """
    logout(request)
    return redirect('login')
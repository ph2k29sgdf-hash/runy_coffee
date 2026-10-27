from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from .models import Product, Location, Review
from .forms import OrderForm, SupportForm, ReviewForm

# ==========================================
# --- ОСНОВНЫЕ СТРАНИЦЫ ---
# ==========================================

def home(request):
    return render(request, 'home.html')

def all_menu(request, category_slug=None):
    if category_slug:
        products = Product.objects.filter(category=category_slug)
    else:
        products = Product.objects.all()
    return render(request, 'menu.html', {'products': products, 'current_category': category_slug})

def new_items(request):
    products = Product.objects.filter(is_new=True)
    return render(request, 'new.html', {'products': products})

def support(request):
    return render(request, 'support.html', {
        'support_phone': settings.SUPPORT_PHONE,
        'support_email': settings.SUPPORT_EMAIL
    })

# ==========================================
# --- ЛОКАЦИИ И ОТЗЫВЫ ---
# ==========================================

def locations(request):
    locs = Location.objects.all()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            location_id = request.POST.get('location_id')
            if location_id:
                review.location_id = location_id
                review.save()
                messages.success(request, "Спасибо! Ваш отзыв опубликован.")
            return redirect('locations')
    else:
        form = ReviewForm()

    return render(request, 'locations.html', {'locations': locs, 'form': form})

# ==========================================
# --- ДОСТАВКА И ЗАКАЗЫ ---
# ==========================================

def delivery(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    if cart:
        products = Product.objects.in_bulk(cart.keys())
        for product_id, quantity in cart.items():
            product = products.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart_items:
                summary = ", ".join([f"{item['product'].name} x{item['quantity']}" for item in cart_items])
                order.items_summary = summary
            else:
                order.items_summary = "Клиент ничего не выбрал"

            order.save()
            request.session['cart'] = {}
            messages.success(request, "Заказ принят! Мы свяжемся с вами.")
            return redirect('home')
    else:
        form = OrderForm()

    return render(request, 'delivery.html', {
        'form': form,
        'support_phone': settings.SUPPORT_PHONE,
        'cart_items': cart_items,
        'total_price': total_price
    })

# ==========================================
# --- АВТОРИЗАЦИЯ ---
# ==========================================

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# ==========================================
# --- ЛОГИКА КОРЗИНЫ ---
# ==========================================

def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def decrease_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
        request.session['cart'] = cart
    return redirect(request.META.get('HTTP_REFERER', 'menu'))

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart
    return redirect('cart_detail')

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    if cart:
        products = Product.objects.in_bulk(cart.keys())
        for product_id, quantity in cart.items():
            product = products.get(int(product_id))
            if product:
                item_total = product.price * quantity
                total_price += item_total
                cart_items.append({'product': product, 'quantity': quantity, 'item_total': item_total})

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

# ==========================================
# --- ЧАТ ПОДДЕРЖКИ (API) ---
# ==========================================

def send_support_message(request):
    if request.method == 'POST':
        form = SupportForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

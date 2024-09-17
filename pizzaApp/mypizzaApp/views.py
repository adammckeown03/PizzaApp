from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PizzaForm, OrderForm, UserLoginForm, UserSignupForm
from .models import Order, User
from django.contrib.auth import logout, login, authenticate


def index(request):
    return render(request, 'index.html')

def loginPage(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)  
            if user is not None:
                login(request, user)
                return redirect('view_orders')
            else:
                messages.error(request, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})



def create_user(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']  # Retrieve email from the form
            username = email  # Use email as username
            password = form.cleaned_data['password1']
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login')  # Redirect to login page after successful registration
    else:
        form = UserSignupForm()
    return render(request, 'create_user.html', {'form': form})

@login_required
def view_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'view_orders.html', {'orders': orders})

@login_required
def create_order(request):
    order = None
    if request.method == 'POST':
        pizza_form = PizzaForm(request.POST)
        order_form = OrderForm(request.POST)
        if pizza_form.is_valid() and order_form.is_valid():
            pizza = pizza_form.save()
            order = order_form.save(commit=False)
            order.user = request.user
            order.pizza = pizza
            order.save()
            messages.success(request, 'Order placed successfully!')
            return redirect('view_order_details', order_id=order.pk)
    else:
        pizza_form = PizzaForm()
        order_form = OrderForm()

    return render(request, 'create_order.html', {'pizza_form': pizza_form, 'order_form': order_form, 'order': order})

@login_required
def view_order_details(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(request, 'order_details.html', {'order': order})

def logout_view(request):
    logout(request)
    return redirect('login')
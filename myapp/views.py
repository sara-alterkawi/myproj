# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, OrderHistory
from django.db import IntegrityError
import json
from django.contrib import messages
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

@login_required(login_url='login')
def HomePage(request):
    if request.method == 'POST':
        user = User.objects.get(username='admin')
        click_data = request.POST.get('clickData',"")
        # print(click_data_json)
        # click_data = json.loads(click_data_json)

        history = {
            'user': request.user,
            'user_name': request.user.username,
        }

        clicked_items = []

        for letter in click_data:
            # value = request.POST.get(letter)
            value = 1
            print(letter,value)
            if value:
                count = getattr(user, letter)
                value = int(value)
                if count - value < 0:
                    message = f"You don't have enough '{letter}' to complete the order"
                    messages.error(request, message)
                    history.update({
                        'error': message,
                        'is_error': True,
                        letter: value
                    })
                    OrderHistory.objects.create(**history)
                    return redirect('home')

                history[letter] = value
                clicked_items.extend([letter] * value)

        history['click_data'] = ''.join(clicked_items)
        print(clicked_items)
        history_instance = OrderHistory.objects.create(**history)
        send_order_update_message(history_instance, user.id, history_instance.id)
        messages.success(request, "Order successfully placed.")
        return redirect('home')

    return render(request, 'home.html')

# Extracted the message sending functionality into a function
def send_order_update_message(order_history, user_id, order_id):
    channel_layer = get_channel_layer()
    message_data = {
        "userid": user_id,
        "orderid": order_id,
        "click_data": getattr(order_history,"click_data")
    }
    # print(getattr(order_history,"click_data"))
    # print(message_data)

    async_to_sync(channel_layer.group_send)(
        "raspberry_pi",
        {
            "type": "raspberry_pi.message",
            "message": message_data
        }
    )

def Signup(request):
    if request.method == 'POST':
        email, password_1, password_2 = request.POST.get('email'), request.POST.get('password1'), request.POST.get('password2')

        if password_1 != password_2:
            messages.error(request, "Your password and confirmation password do not match.")
            return redirect('signup')

        try:
            user = User.objects.create_user(username=email, password=password_1)
            user.save()
        except IntegrityError:
            messages.error(request, "Username (email) is already in use.")
            return redirect('signup')

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('login')

    return render(request, 'signup.html')

def Login(request):
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or Password is incorrect!!!")
            return redirect('login')

    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('login')

def AboutPage(request):
    return render(request, 'about.html')

def OrderPage(request):
    orders = OrderHistory.objects.filter(user=request.user).order_by('-date')    
    return render(request, 'order.html', {'orders': orders})

def RasPi(request):
    return render(request, "raspi.html")
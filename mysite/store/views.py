# 15-04-2025
from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

import csv
import os


# libs for user identification ------------------------------------------------
# app/views.py
import hashlib
import hmac
import urllib.parse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import TelegramUser
# --------  end ---------------------------------------------------------------



def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, ("You have been logged in!"{username}))
            messages.success(request, f"Assalaumagaleikum, {username}! You have been logged in!")
            return redirect('home')
        else:
            messages.success(request, ("There was an error, please try again."))
            return redirect('login')
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    username = request.user.username  # сохраняем имя пользователя до выхода
    logout(request)
    messages.success(request, (f"Sau bolynyz, {username}! You have been logged out. Thanks!"))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have Registered successfully! Welcome!"))
            return redirect('home')
        else:
            messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
            return redirect('register')
    else:
        return render(request, 'register.html', {'form':form})



def product(request,pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})



def category(request, foo):
    # replace hyphens with spaces
    foo = foo.replace('-', ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
    except:
        messages.success(request, ("That category doesn't exists"))
        return redirect('home')










# --------------------------    user identification
@csrf_exempt
def save_user1(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        init_data = data.get('initData')

        if not init_data:
            return JsonResponse({'error': 'Missing initData'}, status=400)

        # Проверка подписи
        if not check_telegram_auth(init_data, settings.TELEGRAM_BOT_TOKEN):
            return JsonResponse({'error': 'Invalid auth'}, status=403)

        parsed_data = dict(urllib.parse.parse_qsl(init_data))
        user_info = json.loads(parsed_data.get('user'))
        user_id = user_info['id']

        # Сохраняем или обновляем пользователя
        TelegramUser.objects.update_or_create(
            telegram_id=user_id,
            defaults={
                'username': user_info.get('username'),
                'first_name': user_info.get('first_name'),
                'last_name': user_info.get('last_name'),
            }
        )

        return JsonResponse({'status': 'ok', 'user_id': user_id})

    return JsonResponse({'error': 'Invalid method'}, status=405)

def check_telegram_auth1(init_data, bot_token):
    parsed_data = dict(urllib.parse.parse_qsl(init_data))
    hash_received = parsed_data.pop('hash', '')

    data_check_string = '\n'.join(
        f'{k}={v}' for k, v in sorted(parsed_data.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_string = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    return hmac_string == hash_received


def profile_user(request):
    return render(request, 'profile_user.html')


# test purpose
@csrf_exempt
def save_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            init_data = data.get('initData')

            if not init_data:
                return JsonResponse({'error': 'Missing initData'}, status=400)

            # Пропускаем проверку подписи!
            parsed_data = dict(urllib.parse.parse_qsl(init_data))
            user_info = json.loads(parsed_data.get('user'))
            user_id = user_info['id']

            # Сохраняем или обновляем пользователя
            TelegramUser.objects.update_or_create(
                telegram_id=user_id,
                defaults={
                    'username': user_info.get('username'),
                    'first_name': user_info.get('first_name'),
                    'last_name': user_info.get('last_name'),
                }
            )

            return JsonResponse({'status': 'ok', 'user_id': user_id})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)


# ----------------------------------        new funcs
@csrf_exempt
def save_user3(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            init_data = data.get('initData')

            if not init_data:
                return JsonResponse({'error': 'Missing initData'}, status=400)

            # Печатаем initData и токен в консоль
            print('--- INIT DATA ---')
            print(init_data)
            print('--- TELEGRAM_BOT_TOKEN ---')
            print(settings.TELEGRAM_BOT_TOKEN)

            # Проверяем подпись
            if not check_telegram_auth(init_data, settings.TELEGRAM_BOT_TOKEN):
                print('--- AUTH CHECK FAILED ---')
                return JsonResponse({'error': 'Invalid auth'}, status=403)
            else:
                print('--- AUTH CHECK PASSED ---')

            parsed_data = dict(urllib.parse.parse_qsl(init_data))
            user_info = json.loads(parsed_data.get('user'))
            user_id = user_info['id']

            TelegramUser.objects.update_or_create(
                telegram_id=user_id,
                defaults={
                    'username': user_info.get('username'),
                    'first_name': user_info.get('first_name'),
                    'last_name': user_info.get('last_name'),
                }
            )

            return JsonResponse({'status': 'ok', 'user_id': user_id})

        except Exception as e:
            print('--- ERROR ---')
            print(str(e))
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)

def check_telegram_auth(init_data, bot_token):
    parsed_data = dict(urllib.parse.parse_qsl(init_data))
    hash_received = parsed_data.pop('hash', '')

    data_check_string = '\n'.join(
        f'{k}={v}' for k, v in sorted(parsed_data.items())
    )

    secret_key = hashlib.sha256(bot_token.encode()).digest()
    hmac_string = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

    print('--- DATA CHECK STRING ---')
    print(data_check_string)
    print('--- SECRET KEY (SHA256 bot_token) ---')
    print(secret_key.hex())
    print('--- GENERATED HMAC STRING ---')
    print(hmac_string)
    print('--- RECEIVED HASH FROM TELEGRAM ---')
    print(hash_received)

    return hmac_string == hash_received



# read CSV and render
def show_csv_table1(request):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        rows = list(reader)

    return render(request, 'table.html', {
        'headers': headers,
        'rows': rows
    })


# read func 2
def show_csv_table(request):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data.csv')
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        sample = csvfile.read(1024)
        csvfile.seek(0)
        dialect = csv.Sniffer().sniff(sample)
        reader = csv.reader(csvfile, dialect)
        headers = next(reader)
        rows = list(reader)

    return render(request, 'table.html', {
        'headers': headers,
        'rows': rows
    })

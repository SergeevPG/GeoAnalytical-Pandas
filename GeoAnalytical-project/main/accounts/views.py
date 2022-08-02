from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        # Массивы для проверки на заполнение полей
        form_data_arr = []
        labels_name_arr = ['\'Имя\'', '\'Фамилия\'', '\'Придумайте логин\'',
                           '\'Введите почту\'', '\'Придумайте пароль\'', '\'Повторите пароль\'']

        first_name = request.POST['first_name']
        form_data_arr.append(first_name)

        last_name = request.POST['last_name']
        form_data_arr.append(last_name)

        username = request.POST['username']
        form_data_arr.append(username)

        email = request.POST['email']
        form_data_arr.append(email)

        password1 = request.POST['password1']
        form_data_arr.append(password1)

        password2 = request.POST['password2']
        form_data_arr.append(password2)

        # Проверка на заполнение полей
        counter = 0
        errors_counter = 0
        for i in form_data_arr:
            i = i.split()
            if not i:
                error_message = f'Заполните поле {labels_name_arr[counter]}'
                messages.info(request, error_message)
                counter += 1
                errors_counter += 1
            else:
                counter += 1
        if errors_counter != 0:
            return redirect('register')

        if password1 != password2:
            # Вывод ошибки несовпадения паролей в форме регистрации
            messages.info(request, 'Пароли не совпадают')
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            # Вывод ошибки неуникальности логина в форме регистрации
            messages.info(
                request, 'Пользователь с таким логином уже существует')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            # Вывод ошибки неуникальности почты в форме регистрации
            messages.info(
                request, 'Пользователь с такой почтой уже существует')
            return redirect('register')
        else:
            # создаем нового пользователя в БД
            user = User.objects.create_user(
                username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('login')
            # return redirect('success_registration')
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        form_data_arr = []
        labels_name_arr = ['\'Логин\'', '\'Пароль\'']

        username = request.POST['username']
        form_data_arr.append(username)

        password = request.POST['password']
        form_data_arr.append(password)

        # Проверка на заполнение полей
        counter = 0
        errors_counter = 0
        for i in form_data_arr:
            i = i.split()
            if not i:
                error_message = f'Заполните поле {labels_name_arr[counter]}'
                messages.info(request, error_message)
                counter += 1
                errors_counter += 1
            else:
                counter += 1
        if errors_counter != 0:
            return redirect('login')

        # Проверка на нахождения пользователя в БД
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # осуществление входа пользователя и переадресация на главную страницу сайта
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Неверный логин или пароль')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    return redirect('home')

# def success_registration(request):
#     return render(request, 'accounts/success_registration.html')
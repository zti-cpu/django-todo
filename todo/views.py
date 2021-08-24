from django.shortcuts import render, redirect, get_object_or_404  # для отправки на новую стрницу
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm  # сохранение формы
from django.contrib.auth.models import User  # созданеи пользователей
from django.db import IntegrityError  # перехват ошибки
from django.contrib.auth import login, logout, authenticate  # создание кабинета пользователя
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required  # возращает что только зареганые могут пользоваться


# Create your views here.
def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":  # если get запрос то открывается страница
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:  # если пост то выполняется сохранение паролей
        if request.POST['password1'] == request.POST['password2']:  # если пороли одинраковые
            try:  # если ошибки нету
                user = User.objects.create_user(request.POST['username'],
                                                password=request.POST['password1'])  # Сохранение
                user.save()
                login(request, user)  # вход в страницу профиля
                return redirect('currenttodos')  # перенаправление на новую страницу после удапчного залогонился
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), "error": "Это имя уже используется"})
        else:  # если пароли разные
            return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), "error": 'Пароли не совподают'})
            # сообщить о несоответсвие поролей


def loginuser(request):  # вход пользователя
    if request.method == "GET":  # если get запрос то открывается страница
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:  # если пост то выполняется вход
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), "error": 'Такого пользователя нет или пароль не верный'})
        else:
            login(request, user)  # вход в страницу профиля
            return redirect('currenttodos')


@login_required
def logoutuser(request):
    if request.method == 'POST':  # ЕСЛИ метод только пост
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=True)
    # передает в базе только данные соответствущего пользователя, datecompleted__isnull проверяет былали завершена задача
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)  # создание формы
            newtodo = form.save(commit=False)  # привязка формы к определенному человек
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Переданы неверные данные'})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,
                             user=request.user)  # передает в базе только данные соответствущего пользователя, datecompleted__isnull проверяет былали завершена задача request.user - веряет автора, чтобы не допустить показ чужой инфы
    if request.method == "GET":
        form = TodoForm(instance=todo)  # изменение гтовой формы
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:  # есои наживают на кнопку изменения формы
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Не верная информация'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,
                             user=request.user)
    if request.method == "POST":
        todo.datecompleted = timezone.now()  # заполняет поле текущей датой при выполнении задачи
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk,
                             user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect('currenttodos')


def completedtodos(request):
    todos = Todo.objects.filter(user=request.user,
                                datecompleted__isnull=False).order_by(
        '-datecompleted')  # сортировка по дате order_by('datecompleted')
    # передает в базе только данные соответствущего пользователя, datecompleted__isnull проверяет былали завершена задача
    return render(request, 'todo/completedtodos.html', {'todos': todos})

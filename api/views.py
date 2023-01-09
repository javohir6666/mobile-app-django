import datetime
from django.shortcuts import render, redirect
from rest_framework import generics
from django.http import HttpResponseRedirect, HttpResponse
from .models import Todo
from django.urls import reverse_lazy
from .serializers import TodoSerializer
from .forms import TodoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url='/login/')
def index(request):
    page_title = 'Todo List'
    todos = Todo.objects.all()
    todo_count = Todo.objects.all().count()
    context = {
        'todos': todos,
        'page_title': page_title,
    }
    if request.user.is_superuser == True:
        today = datetime.date.today()
        tomorrow = today + datetime.timedelta(days=1)
        user_count = User.objects.all().count()
        today_users = User.objects.filter(date_joined__contains=today).count()
        today_todos = Todo.objects.filter(created_at__contains=today).count()
        todos = Todo.objects.all()
        todo_count = Todo.objects.all().count()
        print("Count of TODO: ", todo_count)
        context = {
            "user_count": user_count,
            "todos": todos,
            "todo_count": todo_count,
            "today_users": today_users,
            "today_todos": today_todos,
        }
        return render(request, 'admin_templates/admin.html', context)
    else:
        return render(request, 'index.html', context)


@login_required(login_url='/login/')
def create(request):
    form = TodoForm()
    page_title = 'Todo List'
    if request.method == "POST":
        #Get the posted form
        form = TodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("create")
    return render(request, "create.html", {
        "form": form,
        "page_title": page_title
    })


@login_required(login_url='/login/')
def isDone(request, pk):

    if request.method == 'POST':
        print('alive')
        todo = Todo.objects.get(pk=pk)
        todo.isDone = True
        todo.save()

    return redirect('index')


class TodoGetCreate(generics.ListCreateAPIView, LoginRequiredMixin):
    login_url = '/login/'
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

class TodoUpdateDelete(generics.RetrieveUpdateDestroyAPIView,
                       LoginRequiredMixin):
    login_url = '/login/'
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer


class TodoDeleteView(DeleteView, LoginRequiredMixin):
    login_url = '/login/'
    model = Todo
    template_name = 'delete.html'
    success_url = reverse_lazy('index')

    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.pk


class TodoEditView(UpdateView, LoginRequiredMixin):
    login_url = '/login/'
    model = Todo
    fields = ['title', 'desc']
    template_name = 'edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('detail', kwargs={'pk': pk})

    def test_func(self):
        todo = self.get_object()
        return self.request.user == todo.pk


class TodoDetailView(View, LoginRequiredMixin):
    login_url = '/login/'

    def get(self, request, pk, *args, **kwargs):
        page_title = 'To do Detail'
        post = Todo.objects.get(pk=pk)
        form = TodoForm()

        context = {
            'todo': post,
            'form': form,
            'page_title': page_title,
        }

        return render(request, 'detail.html', context)


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser == True:
                return render(request, 'admin_templates/admin.html')
            return redirect("index")
        else:
            return HttpResponse("Username or password is incorrect")

    return render(request, 'login.html')


def signupPage(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            return HttpResponse("Passwords don't match")
        else:
            my_user = User.objects.create_user(username,
                                               email,
                                               password,
                                               last_name=last_name,
                                               first_name=first_name)
            my_user.save()

        return HttpResponse("User has been created successfully")
    return render(request, 'signup.html')


def logOut(request):
    logout(request)
    return redirect('login')


#ADMIN PAGE
@login_required(login_url='/login/')
def user_list(request):
    if request.user.is_superuser == True:
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'admin_templates/user_list.html', context)
    message = "You are not administrator"
    context = {"message": message}
    return render(request, "index.html", context)


def user_create(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        is_staff = request.POST.get('is_staff')
        is_active = request.POST.get('is_active')
        is_superuser = request.POST.get('is_superuser')
        if password != password2:
            return HttpResponse("Passwords don't match")
        else:
            user_exist = User.objects.filter(username=username).exists()
            email_exist = User.objects.filter(email=email).exists()
            if not user_exist or not email_exist:
                my_user = User.objects.create_user(username,
                                                   email,
                                                   password,
                                                   last_name=last_name,
                                                   first_name=first_name,
                                                   is_staff=is_staff=="on" if True else False,
                                                   is_active=is_active=="on" if True else False,
                                                   is_superuser=is_superuser=="on" if True else False)
                my_user.save()
                return HttpResponse("User has been created successfully")
            else:
                return HttpResponse("Username or email already exists")
    return render(request, 'admin_templates/create_user.html')


@login_required(login_url='/login/')
def todo_list(request):
    if request.user.is_superuser == True:
        todos = Todo.objects.all()
        context = {
            "todos": todos,
        }
        return render(request, 'admin_templates/todo_list.html', context)
    message = "You are not administrator"
    context = {"message": message}

    return render(request, "index.html", context)


@login_required(login_url='/login/')
def todo_search(request):
    if request.user.is_superuser == True:
        query = request.GET.get('query')
        todo_list = Todo.objects.filter(title__icontains=query)

        context = {
            'todo_list': todo_list,
        }

        return render(request, 'admin_templates/todo_list.html', context)
    message = "You are not administrator"
    context = {"message": message}
    return render(request, "index.html", context)


@login_required(login_url='/login/')
def user_search(request):
    if request.user.is_superuser == True:
        query = request.GET.get('query')
        user_list = User.objects.filter(username__icontains=query)

        context = {
            'user_list': user_list,
        }

        return render(request, 'admin_templates/user_list.html', context)
    message = "You are not administrator"
    context = {"message": message}
    return render(request, "index.html", context)


@login_required(login_url='/login/')
def edit_user(request):
    if request.user.is_superuser == True:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                return HttpResponse("Passwords don't match")
            else:
                my_user = User.objects.create_user(username,
                                                   email,
                                                   password,
                                                   last_name=last_name,
                                                   first_name=first_name)
                my_user.save()
    message = "You are not administrator"
    context = {"message": message}
    return render(request, "index.html", context)


def todo_create(request):
    if request.user.is_superuser == True:
        if request.method == 'POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            todo = Todo(title=title, desc=desc)
            todo.save()
            return redirect("todo_list")
    return render(request, 'admin_templates/create_todo.html')


def todo_edit(request, pk):
    if request.user.is_superuser == True:
        todo = Todo.objects.get(pk=pk)
        context = {"todo": todo}
        if request.method == 'POST':
            title = request.POST.get('title')
            desc = request.POST.get('desc')
            todo.title = title
            todo.desc = desc
            todo.save()
            return redirect("todo_list")
    return render(request, 'admin_templates/edit_todo.html', context)


def todo_delete(request, pk):
    if request.user.is_superuser == True:
        todo = Todo.objects.get(pk=pk)
        context = {"todo": todo}
        if request.method == 'POST':
            todo.delete()
            return redirect("todo_list")
    return render(request, 'admin_templates/delete_todo.html', context)
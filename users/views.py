from django.shortcuts import render,redirect
from .forms import LoginForm,SignUpForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            print('user created')
            return redirect('login')
        else:
            messages.error(request,"Username is already taken")
    else:
        form = SignUpForm()
    return render(request,'register1.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('add')
            elif user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request,"Username or password is incorrect")
        else:
            print('error validating form')
    return render(request, 'login2.html', {'form': form, 'msg': msg})

def logout_page(request):
    logout(request)
    return redirect('login')     


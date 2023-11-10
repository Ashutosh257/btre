from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

from inquiry.models import Inquiry

def register(req):
    if req.method == 'POST':
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        password2 = req.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(req, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(req, 'That email is being used')
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password,email=email, first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(req, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(req, 'Passwords do not match')
            return redirect('register')
    else:
            return render(req, 'accounts/register.html')

def login(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(req, user)
            messages.success(req, message='You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(req, message='Invalid credentials')
            return redirect('login')
        
    else:
        return render(req, template_name="accounts/login.html")

def logout(req):

    if req.method == "POST":
        auth.logout(req)
        messages.success(req, message="You have successfully logged out!")
        return redirect('index')

def dashboard(req):

    inquiries = Inquiry.objects.filter(user_id=req.user.id).order_by('-inquiry_date')

    context = {
        "inquiries": inquiries,
        "user_data": req.user
    }
    return render(req, template_name="accounts/dashboard.html", context=context)

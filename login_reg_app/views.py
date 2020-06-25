from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

def index(request):
    context = {
        'allusers': User.objects.all()
    }
    return render(request, 'index.html', context)

def register(request):
    print(request.POST)
    responsefromValidator = User.objects.registerValidator(request.POST)
    print(responsefromValidator)
    if len(responsefromValidator) > 0:
        for key, value in responsefromValidator.items():
            messages.error(request, value)
        return redirect('/')
    else:
        securepassword = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        print(securepassword)
        newuser = User.objects.create(firstname = request.POST['firstname'], lastname = request.POST['lastname'], email = request.POST['email'], password = securepassword)
        request.session['loggedinID'] = newuser.id
        return redirect('/success')

def success(request):
    if 'loggedinID' not in request.session:
        return redirect('/')
    loggedinuser = User.objects.get(id= request.session['loggedinID'])
    context = {
        'loggedinuser': loggedinuser
    }
    return render(request, 'success.html', context)

def login(request):
    print(request.POST)
    loginerrors = User.objects.loginValidator(request.POST)
    if len(loginerrors) >0:
        for key, value in loginerrors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        loggedUser = User.objects.filter(email = request.POST['email'])[0]
        print(loggedUser)
        request.session['loggedinID'] = loggedUser.id
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

# Create your views here.

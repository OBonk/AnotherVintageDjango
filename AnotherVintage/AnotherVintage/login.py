from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from email.utils import parseaddr
from . import views

def loginRQ(request):
    if request.method =="POST":
        username = request.POST.get("username")
        pwd = request.POST.get("password")
        print(username +" "+pwd)
        user = authenticate(request, username=username, password=pwd)
        print(user)
        if user is not None:
            login(request,user)
            if user.groups.filter(name='controller').exists():
                return redirect("stock")
            else:
                return render(request,"home.html")
        else:
            return render(request,"login.html",{"Warning":"Incorrect username or password"})


    else:
        return render(request,"login.html")

def logoutRQ(request):
    if request.user != None:
        logout(request)

    return render(request,"home.html")#

def registerRQ(request):
    if request.method == "POST":
        if not request.POST.get("username"):
            return render(request,"register.html",{"Warning":"username is required!"})
        elif not request.POST.get("firstname"):
            return render(request,"register.html",{"Warning":"first name is required!"})
        elif not request.POST.get("lastname"):
            return render(request,"register.html",{"Warning":"last name is required!"})
        elif not request.POST.get("password"):
            return render(request,"register.html",{"Warning":"password is required!"})
        elif not request.POST.get("email") or parseaddr(request.POST.get("email")) == ('', ''):
            return render(request,"register.html",{"Warning":"valid email is required!"})
        
        user = User.objects.create_user(request.POST.get("username"), request.POST.get("email"), request.POST.get("password"),last_name=request.POST.get("lastname"),first_name=request.POST.get("firstname"))
        login(request,user)
        return render(request,"home.html")
    else:
        return render(request,"register.html")
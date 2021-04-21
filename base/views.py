from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from base.filter import UserFilter
from django.contrib.auth.hashers import make_password

# Create your views here.
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def user_login(request):
    if request.session.has_key('logged'):
        return redirect('home')

    elif request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            request.session['logged']=True
           
            return redirect('home')
        else:
            messages.error(request,'Invalid username or password')
            return render(request,'login.html')    

    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if(User.objects.filter(username=username)).exists():
            return render(request,'register.html',{'error': "Username already avialable"})
        else:


            user = User.objects.create_user(username=username,email=email,password=password,first_name=first_name)
            # user.save()
        
            return redirect('login')

    else:
        
        return render(request,'register.html')

         
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
   
    if request.session.has_key('logged'):
        return render(request,'home.html')
    else:
        return redirect('login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    del request.session['logged']
    return redirect('login')
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_panel(request):

    if request.session.has_key('is_logged'):

        # user = User.objects.all()
        user = User.objects.exclude(is_superuser=1)
        user_filter = UserFilter(request.GET,queryset=user)
        return render(request,'admin_panel.html',{'users':user_filter})
    else:
        return redirect('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_user(request):
    if request.session.has_key('is_logged'):

        if request.method == 'POST':
            first_name=request.POST['first_name']
            username=request.POST['username']
            email=request.POST['email']
            password=request.POST['password']
            if(User.objects.filter(username=username)).exists():
                return render(request,'adduser.html',{'error': "Username already avialable"})
            else:    
                users=User.objects.create_user(first_name=first_name,username=username,email=email,password=password)
                users.save()

                return redirect('admin_panel')
        else:
            return render(request,'adduser.html')
    else:
        return redirect('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_user(request,id):
    if request.session.has_key('is_logged'):
        user = User.objects.get(id=id)
        user.delete()

        messages.error(request,"deleted successfully")
        return redirect("admin_panel")
    else:
        return redirect('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def update_user(request,id):
    if request.session.has_key('is_logged'):
        user = User.objects.get(id=id)
        if request.method == 'POST':
        
            first_name = request.POST['first_name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']

            user.first_name=first_name
            user.username=username
            user.email =email
            user.password= make_password(user.password)

            
            user.save()

            messages.success(request,"Updated Successfully.......")
            return redirect("admin_panel")

        else: 
            return render(request,"user_edit.html",{'user':user}) 
    else:
        return redirect('admin_login')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_login(request):
    if request.session.has_key('is_logged'):
        return redirect('admin_panel')

    elif request.method=='POST':
        uname="admin"
        pwd="admin"

        username=request.POST['username']
        password=request.POST['password']

        if username==uname and password==pwd:
            request.session['is_logged']=True
            return redirect('admin_panel')
        else:
            messages.error(request,'Invalid username or password')
            return redirect('admin_login')
    else:
        return render(request,'admin_login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def admin_logout(request):
    del request.session['is_logged']
    return redirect('admin_login')



    
    
        


       









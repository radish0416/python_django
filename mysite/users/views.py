from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import auth
from .forms import RegistrationForm, LoginForm , ProfileForm, PwdChangeForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():  #表单数据正确
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password2']

            '''
            使用内置User自带create_user方法创建用户，不需要使用save()
            如果直接使用objects.create()方法后不需要使用save()
            '''
            #用户注册信息表，使用系统自带的表
            user = User.objects.create_user(username=username, password=password, email=email)
            #用户个人资料表，这里就需要进行save保存，这里的表是在model.py里设置的表
            user_profile = UserProfile(user=user)
            user_profile.save()

            return HttpResponseRedirect("/accounts/login/")
    else:
        form = RegistrationForm()

    return render(request, 'users/registration.html', {'form': form})

def login(request):
    if request.method == 'POST':
         form = LoginForm(request.POST)

         if form.is_valid():
             username = form.cleaned_data['username']
             password = form.cleaned_data['password']

             user = auth.authenticate(username=username, password=password)

             if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect(reverse('users:profile', args=[user.id]))

             else:
                # 登陆失败
                return render(request, 'users/login.html', {'form': form,
                               'message': 'Wrong password. Please try again.'})
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

'''
这个是解释器，加上这个以后，用户在没有登录的情况下是不可以访问到个人信息页面的
也就是在登录后的页面方法上面加上这个后就表示该页面是要登录后进行访问的
'''
@login_required
def profile(request, pk):
    #根据用户的pk查询出对应的用户注册信息，每张表中系统会默认设置pk字段，也就是id，查询出后存入user表中
    #get_object_or_404()方法是从数据库中获取用户表User的数据
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/profile.html', {'user': user})

@login_required
def profile_update(request, pk):
    #根据id查询出用户表数据
    user = get_object_or_404(User, pk=pk)
    #根据用户名和密码查询出对应的用户信息表
    user_profile = get_object_or_404(UserProfile, user=user)

    if request.method == "POST":

        form = ProfileForm(request.POST)

        if form.is_valid():
            #将修改的数据存入用户表
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            #将修改的数据存入用户信息表
            user_profile.org = form.cleaned_data['org']
            user_profile.telephone = form.cleaned_data['telephone']
            user_profile.save()

            return HttpResponseRedirect(reverse('users:profile', args=[user.id]))
    else:
        default_data = {'first_name': user.first_name, 'last_name': user.last_name,
                        'org': user_profile.org, 'telephone': user_profile.telephone, }
        form = ProfileForm(default_data)

    return render(request, 'users/profile_update.html', {'form': form, 'user': user})

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/accounts/login/")


#修改密码
@login_required
def pwd_change(request, pk):
    user = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        form = PwdChangeForm(request.POST)

        if form.is_valid():

            password = form.cleaned_data['old_password']
            username = user.username

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_active:
                new_password = form.cleaned_data['password2']
                user.set_password(new_password)
                user.save()
                return HttpResponseRedirect("/accounts/login/")

            else:
                return render(request, 'users/pwd_change.html', {'form': form,
        'user': user, 'message': 'Old password is wrong. Try again'})
    else:
        form = PwdChangeForm()

    return render(request, 'users/pwd_change.html', {'form': form, 'user': user})

def index(request):
    return render(request,'index.html')

def toLogin(request):
    return HttpResponseRedirect('/accounts/login/')

def toRegister(request):
    return HttpResponseRedirect('/accounts/register/')

def blog(request):
    return render(request,'users/blog.html')

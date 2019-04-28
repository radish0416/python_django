"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from users import views


#这里是项目的开始，通过
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('users.urls')), #这里是accounts后面可以跟上users.urls文件里面的所有路由地址，然后根据user.urls里面的规则进行跳转
    path('',views.index),
    path('login/',views.toLogin),
    path('register/',views.toRegister),
    
]

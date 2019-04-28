from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

'''
这里是将后台管理数据的管理字段新增几个字段，也就是在model里面新增的字段，让我们新增的字段也能加入后台管理字段中
'''
admin.site.unregister(User)


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class UserProfileAdmin(UserAdmin):
    inlines = [UserProfileInline, ]


admin.site.register(User, UserProfileAdmin)

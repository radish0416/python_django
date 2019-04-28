from django.contrib.auth.models import User
from django.db import models
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField

'''
由于Django Auth自带的User模型字段有限，我们还需要自定义模型UserProfile对其扩展。
Django Auth模块自带User模型所包含字段
username：用户名
email: 电子邮件
password：密码
first_name：名
last_name：姓
is_active: 是否为活跃用户。默认是True
is_staff: 是否为员工。默认是False
is_superuser: 是否为管理员。默认是False
date_joined: 加入日期。系统自动生成。

自定义的UserProfile模型
user: 与User是1对1关系
org：用户名
telephone: 电话
mod_date: 最后修改日期。系统自动生成

'''

'''
用户信息表也就是UserProfile是内嵌在User表中的，查询出User表的数据也就查询出了UserProfile表的信息
可以通过user.profile得到UserProfile表的数据
'''
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile') #系统自带的User模块

    org = models.CharField(
        'Organization', max_length=128, blank=True)

    telephone = models.CharField(
        'Telephone', max_length=50, blank=True)

    mod_date = models.DateTimeField('Last modified', auto_now=True)

    class Meta:
        verbose_name = 'User Profile'

    def __str__(self):
        return self.user

# class Article(models.Model):
#     """文章模型"""
#     STATUS_CHOICES = (
#         ('d', '草稿'),
#         ('p', '发表'),
#     )

#     title = models.CharField('标题', max_length=200, unique=True)
#     slug = models.SlugField('slug', max_length=60, blank=True)
#     body = RichTextUploadingField('正文')

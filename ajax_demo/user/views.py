from django.shortcuts import render,HttpResponse,redirect
import json
#django框架自带的form表单的类
from django import forms
from django.forms import widgets
from django.core.exceptions import NON_FIELD_ERRORS,ValidationError

class LoginForm(forms.Form):
    #在这里进行定义字段属性，类似于modules模块的操作,设置各个字段的类型
    user = forms.CharField(max_length=16,min_length=4,
        # 错误信息是英文，界面显示为中文，在这里设置一下转换，也就是错误字段进行手动翻译为中文，也就是error_messages属性
                           error_messages={
                               "required":"不能为空",
                               "min_length":"最小长度为4",
                               "max_length": "最大长度为16"
                           }
                           )
    pwd = forms.CharField(max_length=16,min_length=8,
                          error_messages={
                              "required": "不能为空",
                              "min_length": "最小长度为8",
                              "max_length": "最大长度为16",
                              "invalid":"格式错误"
                          },
                          #widgets.PasswordInput() 是将密码输入框的输入内容进行密文显示
                          #attrs={"class":"active"}对输入框进行标记，然后在界面上进行css操作，改变样式
                          widget=widgets.PasswordInput(attrs={"class":"active"})
                          )
    age = forms.IntegerField(error_messages={
                               "required":"不能为空",})
    email = forms.EmailField(error_messages={
                               "required":"不能为空",})

    #利用局部钩子函数进行单个字段的自定义检验，局部钩子函数的命名规则是clean_name(name就是字段的名字)
    #取值就是self.cleaned_data.get("name"),val.isdigit()判断是否全为数字
    #局部钩子函数取值只能取对应字段的钩子函数的当前字段或者前面的字段，就相当于user的局部钩子函数取不到pwd的值，在pwd的局部钩子函数中可以取到user的值
    def clean_user(self):
        val = self.cleaned_data.get("user")
        if not val.isdigit():
            return val
        else:
            raise ValidationError('用户名不能全为数字')
    #全局钩子函数，命名规则直接就是clean
    def clean(self):
        user = self.cleaned_data.get("user")
        pwd = self.cleaned_data.get("pwd")
        if user == pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次输入不一致")


# Create your views here.
def index(request):
    return render(request,'index.html')


def ajax_handle(request):
    return HttpResponse('这是无参传递ajax数据')


def cal(request):
    num1 = request.GET.get('num1')
    num2 = request.GET.get('num2')
    num3 = int(num1)+int(num2)
    return HttpResponse(str(num3))


def user_clean(request):
    data={}
    data['is_reg'] = True
    user = request.POST.get('user')
    if user == 'didi':
        pass
    else:
        data['is_reg'] = False
    response = json.dumps(data)
    return HttpResponse(response)

def login(request):
    #从前台界面上传递后台的数据
    if request.method == 'POST':
        print(request.POST)
        form = LoginForm(request.POST)
        #判断数据是否为空，并且判断数据是否符合LoginForm类中的要求
        if form.is_valid():
            #数据不为空并且数据正确
            return HttpResponse("success")
        else:
            #数据至少有一个错误
            all_error = form.errors.get("__all__")  #取出自定义检验规则抛出来的错误

            #locals()函数就是可以把所有的变量传入界面中，{'form':form}是只传入form变量
            # return render(request,'login.html',{'form':form})
            return render(request, 'login.html', locals())
    #第一次跳转login.html文件，此时的form为空
    form = LoginForm()

    return render(request,'login.html',{'form':form})

from django.shortcuts import render, redirect
from django import forms

from app01 import models
from app01.utils.bootstrap import BootStrapForm
from app01.utils.encrypt import md5


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
    )
    password = forms.CharField(
        label='密码',
        # render_value=True，当重定向到当前url时，密码框中保留原来的值
        widget=forms.PasswordInput(render_value=True),
        # widget=forms.PasswordInput,
        required=True,
    )

    # 1⃣️钩子方法，将密码用md5加密
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环ModelForm中的所有字段，给每个字段的插件设置
    #     for name, field in self.fields.items():
    #         # 字段中有属性，保留原来的属性，没有属性，才增加。
    #         if field.widget.attrs:
    #             field.widget.attrs["class"] = "form-control"
    #             field.widget.attrs["placeholder"] = field.label
    #         else:
    #             field.widget.attrs = {
    #                 "class": "form-control",
    #                 "placeholder": field.label
    #             }


def login(request):
    """ 登录 """
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 只要login界面输入用户和密码，form.cleaned_data就能获取到
        # form.cleaned_data = {'username': '12', 'password': '32'}
        # 用了上面的1⃣️钩子方法，显示为{'username': '21', 'password':
        # '20c675e50ef49aba53d4bf5709bd6608'}
        print(form.cleaned_data)

        # 去数据库校验用户名和密码是否匹配(form.cleaned_data是字典对象，里面存了用户名a和密码b，
        # 下面去管理员数据库筛选用户名为a并且密码为b的对象，搜索不到则为none）
        admin_object = models.Admin.objects.filter(**form.cleaned_data).first()
        # 如果对象为none，在密码框下主动添加错误信息
        if not admin_object:
            form.add_error('password', '用户名或密码错误')
            return render(request, 'login.html', {'form': form})
        print('密码正确！')

        # 用户名和密码正确
        # 网站生成随机字符串；写到用户浏览器的cookie中；在写入到session中；
        request.session['info'] = {'id': admin_object.id, 'name': admin_object.username}
        return redirect('/admin/list/')

    return render(request, 'login.html', {'form': form})


def logout(request):
    """ 注销 """

    request.session.clear()

    return redirect('/login/')

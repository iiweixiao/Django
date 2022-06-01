from app01 import models

from django import forms

from django.core.validators import RegexValidator
from django.core.validators import ValidationError

from app01.utils.bootstrap import BootStrapModelForm
from app01.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    """ 校验名字长度 """
    name = forms.CharField(min_length=2, max_length=4, label='用户名')

    class Meta:
        model = models.UserInfo
        # 新增人员时显示的字段
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootStrapModelForm):
    """ 校验手机号，确保新增的手机号不存在 """
    # 验证：方式1 字段+正则方法
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'status', 'level']
        fields = '__all__'
        # exclude = ['level']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'})
        # }

    # 验证：方式2 钩子方法
    # def clean_mobile(self):
    #     txt_mobile = self.cleaned_data['mobile']
    #     if len(txt_mobile) != 11:
    #         # 验证不通过
    #         raise ValidationError('格式错误')
    #     # 验证通过，用户输入的值返回
    #     return txt_mobile
    # 用钩子方法判断添加的手机号是否在数据库中
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile


class PrettyEditModelForm(forms.ModelForm):
    """ 校验手机号，确保编辑完的手机号除自身外不存在 """
    # mobile = forms.CharField(disabled=True, label='手机号')
    mobile = forms.CharField(
        label='手机号',
        validators=[RegexValidator(r'^1[3-9]\d{9}', '手机号格式错误'), ],
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'status', 'level']
        # fields = '__all__'
        # exclude = ['mobile']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'})
        # }

    def clean_mobile(self):
        # 当前编辑的那一行的ID，instance.pk(primary key)

        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile


class AdminModelForm(BootStrapModelForm):
    """ 校验名字长度 """
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        # 新增管理员时显示的字段
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    # 用md5给密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    def clean_confirm_password(self):
        print(self.cleaned_data)
        # 比较两遍密码
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致')
        return confirm


class AdminResetModelForm(BootStrapModelForm):
    """ 重置密码 """
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        # 重置密码时显示的字段
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    # 用md5给密码加密
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('不能与以前的密码相同')
        return md5_pwd

    def clean_confirm_password(self):
        print(self.cleaned_data)
        # 比较两遍密码
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError('密码不一致')
        return confirm

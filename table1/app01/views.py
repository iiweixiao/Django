from django.shortcuts import render, redirect
from app01 import models

from django import forms

from django.core.validators import RegexValidator
from django.core.validators import ValidationError

from app01.utils.pagination import Pagination


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    page_object = Pagination(request, queryset)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
    }
    return render(request, 'depart_list.html', context)


def depart_add(request):
    """ 新建部门 """
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list/')


def user_list(request):
    """ 人员列表 """
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2, plus=1)
    context = {
        'queryset': page_object.page_queryset,  # 人员列表
        'page_string': page_object.html(),  # 分页参数
    }
    return render(request, 'user_list.html', context)


class UserModelForm(forms.ModelForm):
    """ 校验名字长度 """
    name = forms.CharField(min_length=3, label='用户名')

    class Meta:
        model = models.UserInfo
        # 新增人员时显示的字段
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']
        # 给输入框添加样式，方法1
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'})
        # }

    # 给输入框添加样式，方法2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环找到所有的插件，添加了class="form-control"
        for name, field in self.fields.items():
            print(name, field)
            # if name == 'password':
            #     continue
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


def user_add(request):
    """ 添加用户 （ModelForm版本） """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    """ 修改用户信息 """
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == 'GET':
        # 根据ID去数据库获取要编辑的那一行数据（对象）
        form = UserModelForm(instance=row_object)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, nid):
    """ 删除用户 """
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list/')


def pretty_list(request):
    """ 靓号列表 """
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
    # q = models.PrettyNum.objects.filter(mobile__contains='99')
    # q = models.PrettyNum.objects.filter(mobile='14119991111')
        data_dict = {'mobile__contains': search_data}
    # q2 = models.PrettyNum.objects.filter(**data_dict)
    # print(q2)
    # select * from 表 order by level desc;  升序asc降序dsc
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')

    page_object = Pagination(request, queryset, page_size=10)
    context = {
        'queryset': page_object.page_queryset,  # 人员列表
        'page_string': page_object.html(),  # 分页参数
        'search_data': search_data,
    }
    return render(request, 'pretty_list.html', context)


class PrettyModelForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

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


def pretty_add(request):
    """ 新建靓号 """
    if request.method == 'GET':
        form = PrettyModelForm()
        return render(request, 'pretty_add.html', {'form': form})
    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_add.html', {'form': form})


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    def clean_mobile(self):

        # 当前编辑的那一行的ID，instance.pk(primary key)

        txt_mobile = self.cleaned_data['mobile']
        exists = models.PrettyNum.objects.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError('手机号已存在')
        return txt_mobile


def pretty_edit(request, nid):
    """ 编辑靓号 """
    row_object = models.PrettyNum.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = PrettyEditModelForm(instance=row_object)
        return render(request, 'pretty_edit.html', {'form': form})
    form = PrettyEditModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')
    return render(request, 'pretty_edit.html', {'form': form})


def pretty_delete(request, nid):
    """ 删除靓号 """
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')

from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination

from app01.utils.form import UserModelForm


def user_list(request):
    """ 人员列表 """
    queryset = models.UserInfo.objects.all()

    page_object = Pagination(request, queryset, page_size=2, plus=1)
    context = {
        'queryset': page_object.page_queryset,  # 人员列表
        'page_string': page_object.html(),  # 分页参数
    }
    return render(request, 'user_list.html', context)


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

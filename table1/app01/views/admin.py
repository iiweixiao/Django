from django.shortcuts import render, redirect

from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm, AdminResetModelForm


def admin_list(request):
    """ 管理员列表 """
    # 检查用户是否已经登录，即检查session中有没有info值
    # request.session['info'] --> {'id': 11, 'name': 'aaa'}
    # info = request.session.get('info')
    # if not info:
    #     return redirect('/login/')
    # 以上用中间件处理

    # 构造搜索
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict = {'username__contains': search_data}
    queryset = models.Admin.objects.filter(**data_dict).order_by('username')
    page_object = Pagination(request, queryset, page_size=5)
    context = {
        'queryset': page_object.page_queryset,
        'page_string': page_object.html(),
        'search_data': search_data,
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """ 新建管理员 """
    title = '新建管理员'

    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)  # {'username': 'qqq', 'password': '111', 'confirm_password': '222'}
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, 'title': title})


def admin_edit(request, nid):
    """ 编辑管理员 """
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = '编辑管理员'
    if request.method == 'GET':
        form = AdminModelForm(instance=row_object)
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, 'change.html', {'form': form, 'title': title})


def admin_delete(request, nid):
    """ 删除管理员 """
    models.Admin.objects.filter(id=nid).delete()
    return redirect('/admin/list/')


def admin_reset(request, nid):
    row_object = models.Admin.objects.filter(id=nid).first()
    if not row_object:
        return redirect('/admin/list/')

    title = fr'{row_object}密码重置'
    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, 'change.html', {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/admin/list')
    return render(request, 'change.html', {'form': form, 'title': title})

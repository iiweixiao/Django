from django.shortcuts import render, redirect

from app01 import models

from app01.utils.pagination import Pagination
from app01.utils.form import AdminModelForm


def admin_list(request):
    """ 管理员列表 """
    data_dict = {}
    search_data = request.GET.get('q', '')
    if search_data:
        data_dict = {'username__contains': search_data}
    queryset = models.Admin.objects.filter(**data_dict).order_by('username')
    page_object = Pagination(request, queryset, page_size=2)
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




    # if request.method == 'GET':
    #     return render(request, 'admin_add.html')
    # username = request.POST.get('username')
    # models.Admin.objects.create(username=username)
    # return redirect('/admin/list/')
    #
    # if request.method == 'GET':
    #     form = AdminModelForm()
    #     return render(request, 'pretty_add.html', {'form': form})
    # form = PrettyModelForm(data=request.POST)
    # if form.is_valid():
    #     form.save()
    #     return redirect('/pretty/list/')
    # return render(request, 'pretty_add.html', {'form': form})

#
#
# def admin_delete(request):
#     """ 删除部门 """
#     nid = request.GET.get('nid')
#     models.Department.objects.filter(id=nid).delete()
#     return redirect('/depart/list/')
#
#
# def admin_edit(request, nid):
#     """ 编辑部门 """
#     if request.method == 'GET':
#         row_object = models.Department.objects.filter(id=nid).first()
#         return render(request, 'depart_edit.html', {'row_object': row_object})
#     title = request.POST.get('title')
#     models.Department.objects.filter(id=nid).update(title=title)
#     return redirect('/depart/list/')

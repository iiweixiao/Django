from django.shortcuts import render, redirect
from app01 import models

from app01.utils.pagination import Pagination

from app01.utils.form import PrettyModelForm, PrettyEditModelForm


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

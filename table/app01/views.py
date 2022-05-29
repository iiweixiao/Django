from django.shortcuts import render, redirect
from app01 import models


def depart_list(request):
    """ 部门列表 """
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    """ 添加部门 """
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get('title')

    models.Department.objects.create(title=title)
    return redirect('/depart/list')


def depart_delete(request):
    """ 删除部门 """
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list')


def depart_edit(request, nid):
    """ 编辑部门 """
    if request.method == 'GET':
        row_object = models.Department.objects.filter(id=nid).first()
        return render(request, 'depart_edit.html', {'row_object': row_object})
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)
    return redirect('/depart/list')


def user_list(request):
    """ 员工管理 """
    queryset = models.UserInfo.objects.all()

    """
    # 用python语法完成员工信息的查询
    # queryset = models.UserInfo.objects.all()
    # for obj in queryset:
    #     print(obj.id, obj.name, obj.password, obj.age, obj.account, obj.create_time.strftime("%Y-%m-%d"),
    #           obj.get_gender_display(), obj.depart.title)
    """
    return render(request, 'user_list.html', {'queryset': queryset})

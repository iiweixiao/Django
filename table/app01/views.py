from django.shortcuts import render
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


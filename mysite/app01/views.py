from django.shortcuts import render, HttpResponse, redirect

from app01.models import Department, UserInfo


def index(request):
    return HttpResponse('欢迎使用！')


def login(request):
    # GET请求
    if request.method == "GET":
        return render(request, "login.html")
    # POST请求
    else:
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        if username == 'root' and password == '123':
            return redirect('https://sspai.com/')
        else:
            return render(request, 'login.html', {'error_msg': '用户名或密码错误'})


def orm(request):
    # 增
    Department.objects.create(title="销售部")
    Department.objects.create(title="IT部")
    Department.objects.create(title="运营部")
    UserInfo.objects.create(name="武沛齐", password="123", age=19)
    UserInfo.objects.create(name="朱虎飞", password="666", age=29)
    UserInfo.objects.create(name="吴阳军", password="666")

    # 删
    UserInfo.objects.filter(id=3).delete()

    # 改
    UserInfo.objects.filter(id=2).update(password=789)

    # 查
    data_list = UserInfo.objects.all()
    for obj in data_list:
        print(obj.id, obj.name, obj.password, obj.age)

    return HttpResponse('成功')


def info_list(request):
    data_list = UserInfo.objects.all()
    return render(request, "info_list.html", {"data_list": data_list})


def info_add(request):
    if request.method == 'GET':
        return render(request, 'info_add.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    age = request.POST.get('age')

    UserInfo.objects.create(name=user, password=pwd, age=age)
    return redirect('/info/list/')


def info_delete(request):
    nid = request.GET.get('nid')
    UserInfo.objects.filter(id=nid).delete()
    return redirect('/info/list/')

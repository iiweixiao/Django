from django.shortcuts import render, HttpResponse, redirect


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

from  app01.models import Department, UserInfo
def orm(request):
    # 测试ORM操作表中的数据
    # Department.objects.create(title='销售部')
    # Department.objects.create(title='IT部')
    # Department.objects.create(title='运营部')
    UserInfo.objects.create(name="武沛齐", password="123", age=19)
    UserInfo.objects.create(name="朱虎飞", password="666", age=29)
    UserInfo.objects.create(name="吴阳军", password="666")
    UserInfo.objects.filter(id=3).delete()
    # Department.objects.all().delete()
    # UserInfo.objects.all().delete()





    return HttpResponse('成功')
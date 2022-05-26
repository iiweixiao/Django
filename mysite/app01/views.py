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

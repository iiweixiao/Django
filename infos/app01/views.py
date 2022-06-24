from django.shortcuts import render, HttpResponse
from app01.models import SougouNewsInfo

from utils.sougou import sougou
from utils.s_email import send_email


def index(request):
    # return HttpResponse('欢迎使用')
    search_data = request.GET.get('k', '')
    page = request.GET.get('p', '1')
    if page == '':
        page = 1
    try:
        page = eval(page)
    except:
        print('page error')
    key_words = []
    print(search_data)
    print(type(search_data))
    if search_data:
        if ',' in search_data:
            key_words = search_data.split(',')
        elif '，' in search_data:
            key_words = search_data.split('，')
        else:
            key_words.append(search_data)
        print(key_words)
        # send_email('"813703110@qq.com"', sougou(key_words), search_data)
        contents, html_query = sougou(key_words, page)
        context = {
            'search_data': search_data,
            'contents': contents,
            'html_query': html_query,
        }

        return render(request, 'index.html', context)
    return render(request, 'index.html')


# 测试orm
def orm(request):
    # 测试ORM操作表中的数据 2011-11-11  datetime.datetime.now()

    # #### 1.新建 ####
    SougouNewsInfo.objects.create(title='百度', href='http://www.baidu.com', source='小小', created='2022/6/6')
    # Department.objects.create(title="销售部")
    # Department.objects.create(title="IT部")
    # Department.objects.create(title="运营部")
    # UserInfo.objects.create(name="武沛齐", password="123", age=19)
    # UserInfo.objects.create(name="朱虎飞", password="666", age=29)
    # UserInfo.objects.create(name="吴阳军", password="666")

    # #### 2.删除 ####
    # UserInfo.objects.filter(id=3).delete()
    # Department.objects.all().delete()

    # #### 3.获取数据 ####
    # 3.1 获取符合条件的所有数据
    # data_list = [对象,对象,对象]  QuerySet类型
    # data_list = UserInfo.objects.all()
    # for obj in data_list:
    #     print(obj.id, obj.name, obj.password, obj.age)

    # data_list = [对象,]
    # data_list = UserInfo.objects.filter(id=1)
    # print(data_list)
    # 3.1 获取第一条数据【对象】
    # row_obj = UserInfo.objects.filter(id=1).first()
    # print(row_obj.id, row_obj.name, row_obj.password, row_obj.age)

    # #### 4.更新数据 ####
    # UserInfo.objects.all().update(password=999)
    # UserInfo.objects.filter(id=2).update(age=999)
    # UserInfo.objects.filter(name="朱虎飞").update(age=999)

    return HttpResponse("成功")

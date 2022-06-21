from django.shortcuts import render

from utils.sougou import sougou
from utils.s_email import send_email


def index(request):
    # return HttpResponse('欢迎使用')
    search_data = request.GET.get('k', '')
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
        contents, html_query = sougou(key_words)
        context = {
            'search_data': search_data,
            'contents': contents,
            'html_query': html_query,
        }

        return render(request, 'index.html', context)
    return render(request, 'index.html')
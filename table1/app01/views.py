from django.shortcuts import render


def depart_list(request):
    return render(request, 'depart_list.html')
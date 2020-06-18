
from django.shortcuts import render, reverse


# 专门处理后台首页-或其他的后台操作
def index(request):
    return render(request, 'myadmin/index.html')

def Demo(request):
    return render(request, 'myadmin/demo.html')
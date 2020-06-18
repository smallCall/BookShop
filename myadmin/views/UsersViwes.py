import random
import time
import os

from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.hashers import *
# 表示在根目录(myadmin)下的当前文件中导入models
from .. import models


# 会员管理-列表
def user_index(request):
    # 通过模型获得数据库中的数据
    data = models.Users.objects.all()
    # 接收搜索条件

    """搜索功能"""
    select_type = request.GET.get('select_type', None)
    key_words = request.GET.get('key_words', None)
    if select_type:
        # 当搜索条件不为空
        if select_type == 'all':
            from django.db.models import Q
            # 参考文档,进行复杂过滤时，需要用到Q这个对象
            # https://docs.djangoproject.com/zh-hans/2.2/topics/db/queries/#complex-lookups-with-q-objects
            data = data.filter(
                Q(id__contains=key_words)
                | Q(User_name__contains=key_words)
                | Q(Phone__contains=key_words)
            )
            # select * from users where id like '%keywords%' or username like '%keywords%' or Phone like '%keywords%'
        # return HttpResponse(f'<script> alert("依据全部搜索");history.go(-1) </script>')
        else:
            search = {f'{select_type}__contains': key_words}
            data = data.filter(**search)
        # return HttpResponse(f'<script> alert("其余"); history.go(-1) </script>')

    """分页功能"""
    # 参考文档https://docs.djangoproject.com/zh-hans/2.2/topics/pagination/
    from django.core.paginator import Paginator
    # 实例分页对象
    p = Paginator(data, 5)
    # 获取当前页码,默认为1
    page_index = request.GET.get('page', 1)
    # 根据页码获得当前页的数据
    data = p.page(page_index)

    # 分配数据
    context = {'data': data}
    # 加载模板
    return render(request, 'myadmin/users/index.html', context=context)


# 会员管理-添加
def user_add(request):
    if request.method == 'GET':
        return render(request, 'myadmin/users/add.html')
    else:
        # 接收来自web的表单数据
        # 相关http请求内属性POST的方法可以参考如下
        # https://docs.djangoproject.com/zh-hans/2.2/ref/request-response/#django.http.QueryDict
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")

        # 对数据进行处理
        # 1.对密码进行加密
        # 相关文档操作
        # https: // docs.djangoproject.com / en / 2.2 / topics / auth / passwords /
        # 要导入 from django.contrib.auth.hashers import *
        data['Pass_word'] = make_password(data['Pass_word'])

        # 2.判断是否有头像上传
        if request.POST.get('Face_url') == '':
            data.pop('Face_url')
            print('没有头像上传')
        else:
            # 上传头像
            # 保存完成后，返回保存文件的路径
            data['Face_url'] = Upload_file(request)
            print(data)
            if not data['Face_url']:
                return HttpResponse(f'<script>alert("头像不符合要求");history.go(-1);</script>')
        # 调用模型，把数据存入数据库中
        try:
            user = models.Users(**data)
            user.save()
            url = reverse('myadmin_user_index')
            print(url, data)
            return HttpResponse(f'<script>alert("添加成功");location.href="{url}"</script>')
        except:
            return HttpResponse(f'<script>alert("添加失败");history.go(-1);</script>')


# 会员管理-删除
def user_delete(request):
    try:
        # 获取需要删除的用户id
        id = request.GET.get('id')
        obj = models.Users.objects.get(id=id)
        # 判断当前用户是否使用的是默认头像，如果是就删除
        print(obj.Face_url)
        if obj.Face_url != '/static/myadmin/img/user05.png':
            # 使用了自己上传的头像，需要删除
            try:
                os.remove('.' + obj.Face_url)
            except:
                return JsonResponse({'error': 2, 'msg': '头像删除失败'})
        # 执行删除
        obj.delete()
        # 返回结果
        return JsonResponse({'error': 0, 'msg': '头像删除成功'})
    except:
        return JsonResponse({'error': 1, 'msg': '头像删除失败'})


# 会员管理-修改
def user_edit(request, uid):
    try:
        obj = models.Users.objects.get(id=uid)
    except:
        return HttpResponse('<script>alert("参数错误");history.go(-1);</script>')
    if request.method == 'GET':
        # 获取用户对象，加载编辑表单
        context = {'userobj': obj}
        return render(request, 'myadmin/users/edit.html', context=context)
    else:
        # 接收表单数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        print(data)
        # 完成数据更新
        # 检测是否有头像进行更新
        if 'Face_url' not in data:
            # 储存头像
            data['Face_url'] = Upload_file(request)
            # 如果以前的头像不是默认头像，就对他进行一个删除
            if obj.Face_url != '/static/myadmin/img/user05.png':
                os.remove('.' + obj.Face_url)

        else:
            data.pop('Face_url')
        obj = models.Users.objects.filter(id=uid).update(**data)
        # 跳转至用户查看界面
        url = reverse('myadmin_user_index')
        return HttpResponse(f'<script>alert("修改成功"); location.href="{url}"</script>')


# 封装函数，进行头像上传
def Upload_file(request, img_name="face"):
    # 上传头像
    my_file = request.FILES.dict().get(img_name)
    if not my_file:
        return False
    # split() 方法 可以按照指定的分隔符，把字符串分隔成列表
    filetype = my_file.name.split('.').pop()

    # 限制上传文件类型
    if filetype not in ['png', 'jpg', 'gif']:
        return HttpResponse(f'<script>alert("上传的文件不符合要求");history.go(-1);</script>')
    # 定义要存储文件的名字
    filename = str(time.time()) + str(random.randint(1000, 99999)) + '.' + filetype
    # 把文件保存到服务器上
    try:
        with open(f'./static/uploads/{filename}', 'wb+') as fp:
            fp.write(my_file.read())
        # 返回当前文件的路径
        return f'/static/uploads/{filename}'
    except:
        return False

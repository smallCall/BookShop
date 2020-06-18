from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from .. import models
from .BooktypeViews import select_all_types
from .UsersViwes import Upload_file


# 图书分类 列表
def Books_index(request):
    # 接收数据
    data = models.Books.objects.all()
    # 访问关联对象参考
    # https: // docs.djangoproject.com / zh - hans / 2.2 / ref / models / relations /
    print(data[0].bookimgs_set.first().Book_img_url)
    context = {'data': data}
    return render(request, 'myadmin/books/index.html', context=context)


# 图书分类 添加
def Books_add(request):
    if request.method == 'GET':
        context = {'types': select_all_types()}
        return render(request, 'myadmin/books/add.html', context=context)
    else:
        # 接收表单数据
        data = request.POST.dict()
        data.pop('csrfmiddlewaretoken')
        # 检测是否上传了图书封面
        if not request.FILES.get('Img_url', None):
            return HttpResponse(f'<script>alert("至少上传一张图片");history.back();</script>')
        try:
            # 添加图书对象
            data['Type_belong'] = models.BookType.objects.get(id=data['Type_belong'])
            book_obj = models.Books(**data)
            book_obj.save()
        except:
            return HttpResponse(f'<script>alert("图书上传失败");history.back();</script>')

        try:
            # 图书封面图的处理
            img_obj = models.BookImgs()
            # 一个图书有多个图书封面
            img_obj.Book_belong = book_obj
            img_obj.Book_img_url = Upload_file(request, 'Img_url')
            img_obj.save()
            print(data)
        except:
            book_obj.delete()
            return HttpResponse(f'<script>alert("图书封面上传失败");history.back();</script>')

        url = reverse('myadmin_Books_index')
        return HttpResponse(f'<script>alert("添加成功");location.href="{url}" </script>')


# 图书分类 删除
def Books_delete(request):
    return render(request, 'myadmin/books/delete.html')


# 图书分类 编辑
def Books_edit(request):
    return render(request, 'myadmin/books/edit.html')

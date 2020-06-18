from django.shortcuts import render, reverse
from django.http import HttpResponse, JsonResponse
from .. import models


# 封装函数，对于查询并返回有层次的set集合对象
def select_all_types():
    data = models.BookType.objects.extra(select={'paths': 'concat(Book_path,id)'}).order_by('paths')
    for i in data:
        # print(type(i), i)
        # <class 'myadmin.models.BookType'> BookType object (1)
        num = i.Book_path.count(',') - 1
        i.nbsp = '|----' * num
        # 如果当前不是是顶级分类，获取他的父级的分类名称
        if i.Book_pid != 0:
            i.p_name = models.BookType.objects.get(id=i.Book_pid).Book_name
    return data


# 图书分类 列表
def BookType_index(request):
    # select * from myadmin_booktype;
    # data = models.BookType.objects.all()
    # select *, contcat(Book_path,id) as paths from myadmin_booktype order by paths;
    # data = models.BookType.objects.extra(select={'paths': 'concat(Book_path,id)'}).order_by('paths')
    # print(type(data), data[0].Book_path)
    # <class 'django.db.models.query.QuerySet'> 0,
    context = {'data': select_all_types()}

    # print(type(context), context['data'])
    # <class 'dict'> < QuerySet[< BookType: BookType object(1) >, < BookType: BookTypeobject(5) >,
    return render(request, 'myadmin/booktype/index.html', context=context)


# 图书分类 添加
def BookType_add(request):
    # select *, contcat(Book_path,id) as paths from myadmin_booktype order by paths;
    types = select_all_types()
    context = {'types': types}
    if request.method == 'GET':
        return render(request, 'myadmin/booktype/add.html', context=context)
    else:
        # 接收表单数据
        data = request.POST.dict()
        data.pop("csrfmiddlewaretoken")
        # {'Book_pid': '1', 'Book_name': '玄幻'}
        # 判断当前添加的分类是否为顶级分类
        if data['Book_pid'] == '0':
            data['Book_path'] = '0,'
        else:
            # {'Book_pid': '2', 'Book_name': '修仙'}
            # path 是父级的path数据加上当前的父级Book_pid
            # 获取父级对象
            obj = types.get(id=data['Book_pid'])
            data['Book_path'] = obj.Book_path + data['Book_pid'] + ','
            # {'Book_pid': '1', 'Book_name': '斗破苍穹', 'Book_path': '0,1,'}

    # 进行数据的添加
    try:
        obj = models.BookType(**data)
        obj.save()
        url = reverse('myadmin_BookType_index')
        # /admin/BookType/index
        return HttpResponse(f'<script>alert("图书分类添加成功");location.href="{url}"</script>')
    except:
        return HttpResponse(f'<script>alert("图书分类添加失败");history.back();"</script>')

    return HttpResponse("BookType_add")


# 图书分类 删除
def BookType_delete(request):
    # 获取要删除的分离的id
    id = request.GET.get('id')
    # 判断当前类下是否含有子类
    num = models.BookType.objects.filter(Book_pid=id).count()
    if num:
        return JsonResponse({'error': 1, 'msg': '该类下含有子类，不能删除'})

    # 判断该类下是否含有商品

    # 执行删除
    try:
        obj = models.BookType.objects.get(id=id)
        obj.delete()
        return JsonResponse({'error': 0, 'msg': '删除成功'})
    except:
        return JsonResponse({'error': 3, 'msg': '删除失败'})


# 图书分类 编辑
def BookType_edit(request):
   try:
        # 接收ajax请求参数,包含了要修改类型的id，以及修改后的名称
        data = request.POST.dict()
        # 获取要修改的对象
        obj = models.BookType.objects.get(id=data['id'])
        obj.Book_name = data['name']
        obj.save()
        return JsonResponse({'error': 0, 'msg': '更新成功'})
   except:
        return JsonResponse({'error': 1, 'msg': '更新失败'})

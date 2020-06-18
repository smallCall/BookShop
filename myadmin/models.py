# Create your models here.
from django.db import models


# 会员 模型
# 相关models方法的参考https://docs.djangoproject.com/zh-hans/2.2/ref/models/fields/#datetimefield
class Users(models.Model):
    User_name = models.CharField(max_length=20)
    Pass_word = models.CharField(max_length=80)
    Phone = models.CharField(max_length=11)
    # 性别不是必填
    Sex = models.IntegerField(null=True)
    Age = models.IntegerField(null=True)
    Add_time = models.DateTimeField(auto_now_add=True)
    # 每次登陆都会更新
    # auto_now 每次都会更新，auto_now_add第一次添加的时候更新
    Save_time = models.DateTimeField(auto_now=True)
    Status = models.IntegerField(default=0)
    # 文件选择，跟目录下的static
    Face_url = models.CharField(max_length=180, default='/static/myadmin/img/user05.png')


# 图书分类模型
class BookType(models.Model):
    Book_name = models.CharField(max_length=10)
    Book_pid = models.IntegerField()
    Book_path = models.CharField(max_length=50)


# 图书商品模型
class Books(models.Model):
    # 一对多，参数：当前类1对多的对象， 级联删除
    # 主外关系键中，级联删除，也就是当删除主表的数据时候从表中的数据也随着一起删除
    Type_belong = models.ForeignKey('BookType', on_delete=models.CASCADE)
    Title = models.CharField(max_length=255)
    Tuijian = models.CharField(max_length=255)
    Author = models.CharField(max_length=50)
    # 出版社
    Publisher = models.CharField(max_length=100)
    # 出版时间
    Pub_date = models.DateTimeField()
    Price = models.FloatField()
    # 库存
    Num = models.IntegerField(default=10)
    Isbn = models.CharField(max_length=13)
    # 详情
    Context = models.TextField()


# 图书封面图集
class BookImgs(models.Model):
    Book_belong = models.ForeignKey('Books', on_delete=models.CASCADE)
    Book_img_url = models.CharField(max_length=100)


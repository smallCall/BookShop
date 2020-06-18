from django.contrib import admin
from django.urls import path,include

from . views import *

urlpatterns = [
    # 后台管理首页
    path('', IndexViews.index, name='myadmin_index'),
    path('Demo/', IndexViews.Demo),

    # 会员管理首页
    path('user/index', UsersViwes.user_index, name='myadmin_user_index'),


    # 会员管理操作
    path('user/add', UsersViwes.user_add, name='myadmin_user_add'),
    path('user/delete', UsersViwes.user_delete, name='myadmin_user_delete'),
    path('user/edit/<int:uid>/', UsersViwes.user_edit, name='myadmin_user_edit'),


    # 图书分类管理首页
    path('BookType/index', BooktypeViews.BookType_index, name='myadmin_BookType_index'),

    # 图书分类管理操作
    path('BookType/add', BooktypeViews.BookType_add, name='myadmin_BookType_add'),
    path('BookType/delete', BooktypeViews.BookType_delete, name='myadmin_BookType_delete'),
    path('BookType/edit', BooktypeViews.BookType_edit, name='myadmin_BookType_edit'),


    # 图书商品管理首页
    path('Books/index', BooksViews.Books_index, name='myadmin_Books_index'),

    # 图商品书管理操作
    path('Books/add', BooksViews.Books_add, name='myadmin_Books_add'),
    path('Books/edit', BooksViews.Books_edit, name='myadmin_Books_edit'),
    path('Books/delete', BooksViews.Books_delete, name='myadmin_Books_delete'),
]
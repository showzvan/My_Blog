#-*-coding:utf-8-*-
from django.urls import path,re_path
from . import views

urlpatterns = [
    # http://localhost:8000/blog/1
    path('', views.blog_list,name='blog_list'),
    path('<int:blog_pk>', views.blog_detail, name='blog_detail'),
    path('type/<int:blogs_type_pk>',views.blogs_with_type,name='blogs_with_type'),
    path('date/<int:year>/<int:month>',views.blogs_with_date, name='block_with_date'),
]
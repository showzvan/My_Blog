from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from django.contrib.contenttypes.models import ContentType
from . models import BlogType,Blog
from django.db.models import Count
from read_statistics.models import ReadNum
from django.conf import settings
from read_statistics.utils import read_statistics_once_read


def get_blog_list_common_data(request,blog_all_list,):
    paginator = Paginator(blog_all_list, settings.EACH_PAGE_BLOGS_NUMBER)  # 每十篇进行分页
    page_num = request.GET.get('page', 1)  # 获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)  # 处理获取到的页码
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码，前后两页的范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('create_time', 'month', order='DESC')
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year=blog_date.year,
                            create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    context = {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'page_range': page_range,
        # 'blog_types': BlogType.objects.annotate(blog_count=Count('blog')), # 获取博客分类的对应博客数量
        'blog_types': BlogType.objects.annotate(blog_count=Count('blog')), # 获取博客分类的对应博客数量
        'blog_dates': blog_dates_dict  # 返回一个固定的日期，得到列表
    }
    return context


def blog_list(request):
    blog_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request,blog_all_list)
    return render_to_response('blog/blog_list.html', context=context)


def blogs_with_type(request,blogs_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blog_type'] = blog_type
    return render_to_response('blog/blog_with_type.html', context=context)

# 按日期分类
def blogs_with_date(request,year,month):
    blog_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context = get_blog_list_common_data(request, blog_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    return render_to_response('blog/blog_with_date.html', context=context)

def blog_detail(request,blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request,blog)

    context = {
        'blog': blog,
        'previous_blog':Blog.objects.filter(create_time__gt=blog.create_time).last(),
        'next_blog':Blog.objects.filter(create_time__lt=blog.create_time).first()
    }
    response = render_to_response('blog/blog_detail.html', context=context) # 响应
    response.set_cookie(read_cookie_key,'true') # 阅读cookie标记
    return response
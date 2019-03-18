from django.shortcuts import render_to_response,get_object_or_404
from django.core.paginator import Paginator
from . models import BlogType,Blog
from django.conf import settings

def blog_list(request):
    blog_all_list = Blog.objects.all()
    paginator = Paginator(blog_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    page_num = request.GET.get('page', 1)  # 获取页码参数(GET请求)
    page_of_blogs = paginator.get_page(page_num)  # 处理获取到的页码
    current_page_num = page_of_blogs.number # 获取当前页码
    # 获取当前页码，前后两页的范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))
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

    context = {
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'page_range':page_range,
        'blog_types': BlogType.objects.all()
    }
    return render_to_response('blog/blog_list.html', context=context)

def blog_detail(request,blog_pk):
    context = {
        'blog':get_object_or_404(Blog, pk=blog_pk)
    }
    return render_to_response('blog/blog_detail.html', context=context)

def blogs_with_type(request,blogs_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blogs_type_pk)
    blog_all_list = Blog.objects.filter(blog_type=blog_type)
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

    context = {
        'blog_type': blog_type,
        'blogs': page_of_blogs.object_list,
        'page_of_blogs': page_of_blogs,
        'page_range': page_range,
        'blog_types': BlogType.objects.all()
    }
    return render_to_response('blog/blog_with_type.html', context=context)


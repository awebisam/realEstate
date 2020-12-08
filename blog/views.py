from django.shortcuts import render
from .models import Blog
from django.core.paginator import Paginator
# Create your views here.


def blog_list(request):
    queryset_list = Blog.blogs.all()
    paginator = Paginator(queryset_list, 6)
    page = request.GET.get('page')
    paged_blogs = paginator.get_page(page)

    context = {
        'blogs': paged_blogs
    }
    return render(request, 'blog/list.html', context)


def blog_detail(request, slug):
    blog = Blog.blogs.get(slug=slug)
    context = {
        'b': blog
    }
    return render(request, 'blog/detail.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .forms import *
from .models import *

menu = [{'title': 'About website', 'url_name': 'about'},
        {'title': 'Add article', 'url_name': 'addpage'},
        {'title': 'Feedback', 'url_name': 'contact'},
        {'title': 'Sign up', 'url_name': 'login'}]


def index(request):
    posts = Women.objects.all()
    context = {'title': 'Main Page',
               'posts': posts,
               'cat_selected': 0,
               }

    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'About Web page', 'menu': menu})


def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPostForm()
    return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Adding an article'})


def contact(request):
    return HttpResponse('feedback')


def login(request):
    return HttpResponse('auth')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>The web-page not found</h1>")


def show_post(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'post': post,
        'menu': menu,
        'title': post.title,
        'cat_selected': post.cat_id,
    }
    return render(request, 'women/post.html', context=context)


def show_category(request, cat_slug):
    cat = Category.objects.filter(slug=cat_slug)
    posts = Women.objects.filter(cat_id=cat[0].pk)
    context = {'title': 'Display by category',
               'posts': posts,
               'cat_selected': cat_slug,
               }
    if len(posts) == 0:
        raise Http404()
    return render(request, 'women/index.html', context=context)

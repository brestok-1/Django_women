from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from .models import *

menu = [{'title': 'About website', 'url_name': 'about'},
        {'title': 'Add article', 'url_name': 'addpage'},
        {'title': 'Feedback', 'url_name': 'contact'},
        {'title': 'Sign up', 'url_name': 'login'}]


def index(request):
    posts = Women.objects.all()
    context = {'title': 'Main Page',
               'menu': menu,
               'posts': posts,
               'cat_selected': 0,
               }

    return render(request, 'women/index.html', context=context)


def about(request):
    return render(request, 'women/about.html', {'title': 'About Web page', 'menu': menu})


def addpage(request):
    return HttpResponse('add article')


def contact(request):
    return HttpResponse('feedback')


def login(request):
    return HttpResponse('auth')


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>The web-page not found</h1>")


def show_post(request, post_id):
    return HttpResponse(f"Show the article with id = {post_id}")


def show_category(request, cat_id):
    posts = Women.objects.filter(cat_id=cat_id)
    context = {'title': 'Display by category',
               'menu': menu,
               'posts': posts,
               'cat_selected': cat_id,
               }
    if len(posts) == 0:
        raise Http404()
    return render(request, 'women/index.html', context=context)

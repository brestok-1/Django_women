from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import *
from .models import *
from .utils import *


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    # extra_context = {'title': 'Main page'}  # For immutable data

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WomenHome, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Main page')
        return dict(list(context.items()) + list(c_def.items()))  # combining dictionaries

    def get_queryset(self):  # We chose what we need to get from the model
        return Women.objects.filter(is_published=True).select_related(
            'cat')  # greedy query to reduce the load on the database


# def index(request):
#     posts = Women.objects.all()
#     context = {'title': 'Main Page',
#                'posts': posts,
#                'cat_selected': 0,
#                'menu': menu
#                }
#
#     return render(request, 'women/index.html', context=context)

# @login_required  # the same as LoginRequiredMixin in classes
# def about(request):
#     contact_list = Women.objects.all()
#     paginator = Paginator(contact_list, 3)
#
#     page_number = request.GET.get('page')
#     paje_obj = paginator.get_page(page_number)
#     cats = Category.objects.annotate(Count('women'))
#     return render(request, 'women/about.html',
#                   {"page": paje_obj, 'title': 'About Web page', 'menu': menu, 'cats': cats})


class AboutPage(DataMixin, ListView):
    model = AboutModel
    template_name = 'women/about.html'
    context_object_name = 'about'
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='About page')
        return context | c_def


# def addpage(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     return render(request, 'women/addpage.html', {'form': form, 'menu': menu, 'title': 'Adding an article'})

class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')  # The same as redirect in functions
    # login_url = reverse_lazy('home')  # if the user is not logged in, redirects to selected url
    raise_exception = True  # if the user isn't logged in, raise 403 error

    def get_context_data(self, **kwargs):
        context = super(AddPage, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Add article')
        return context | c_def


def pageNotFound(request, exception):
    return HttpResponseNotFound("<h1>The web-page not found</h1>")


# def show_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post': post,
#         'title': post.title,
#         'cat_selected': post_slug,
#     }
#     return render(request, 'women/post.html', context=context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # We defined name of our slug (default : slug)
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(ShowPost, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return c_def | context


# def show_category(request, cat_slug):
#     cat = Category.objects.filter(slug=cat_slug)
#     posts = Women.objects.filter(cat_id=cat[0].pk)
#     context = {'title': 'Display by category',
#                'posts': posts,
#                'cat_selected': cat_slug,
#                }
#     if len(posts) == 0:
#         raise Http404()
#     return render(request, 'women/index.html', context=context)
class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'  # rewrite collection 'object_list' to collection 'posts'
    allow_empty = False  # If slug doesn't exist, raise 404 error

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WomenCategory, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title=f'Category - {self.kwargs["cat_slug"]}',
                                      cat_selected=self.kwargs['cat_slug'])
        return context | c_def

    def get_queryset(self):  # We chose what we need to get from the model
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        contex = super(RegisterUser, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Register')
        return contex | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginUser, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Login')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(ContactFormView, self).get_context_data(**kwargs)
        c_def = self.get_user_context(title='Feedback')
        return context | c_def

    def form_valid(self, form):
        return redirect('home')

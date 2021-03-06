from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from women.forms import AddPostForm, RegisterUserForm, LoginUserForm, ContactForm
from women.models import *
from .utils import *

# menu = [
#     {'title': 'О сайте', 'url_name': 'about'},
#     {'title': 'Добавить статью', 'url_name': 'add_page'},
#     {'title': 'Обратная связь', 'url_name': 'contact'},
#     {'title': "Войти", 'url_name': 'login'}
# ]

class WomenHome(DataMixin,ListView):
    paginate_by = 1
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Главная страница')
        context = dict(list(context.items())+ list(c_def.items()))
        return context

    def get_queryset(self):
        return Women.objects.filter(is_published = True).select_related('cat')

# def index(request):
#     posts = Women.objects.all()
#     # cats = Category.objects.all()
#     context = {
#         'posts': posts,
#         # 'cats': cats,
#         'menu': menu,
#         'title': 'Главная страница',
#         'cat_selected': 0,
#     }
#     return render(request, 'women/index.html', context=context)


def about(request):
    contact_list = Women.objects.all()
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'women/about.html', {'page_obj':page_obj, 'menu': menu, 'title': 'О сайте'})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add_page.html'
    success_url = reverse_lazy('home')
    login_url = '/admin/'
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title']='Добавление статьи'
        # context['menu']=menu
        c_def= self.get_user_context(title = 'Добавление статьи')
        return context

def contact(request):
    return HttpResponse('Контактная информация')

#
# def login(request):
#     return HttpResponse('Вход на сайт')


# def read_post(request, post_slug):
#     post = get_object_or_404(Women, slug=post_slug)
#     context={
#         'menu': menu,
#         'post': post,
#         'title': post.title,
#         'cat_selected': post.cat_id
#     }
#     return render(request, 'women/post.html', context)

class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super().get_context_data(**kwargs)
        # context['title']= context['post']
        # context['menu']=menu
        c_def = self.get_user_context(title = context['post'])
        return dict(list(context.items())+list(c_def.items()))

# def show_category(request, cat_id):
#     # cats = Category.objects.all()
#     posts = Women.objects.filter(cat_id=cat_id)
#
#     # if len(posts)==0:
#     #     return Http404()
#     context = {
#         'menu': menu,
#         # 'cats': cats,
#         'cat_selected': cat_id,
#         'posts': posts,
#         'title': "Отображение по рубрикам"
#     }
#     return render(request, 'women/index.html', context=context)

class WomenCategory(DataMixin, ListView):
    # paginate_by = 1
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False


    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] =  menu
        # context['cat_selected'] = context['posts'][0].cat_id
        c_def = self.get_user_context(title ='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)

        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title = 'Регистрация')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title = 'Авторизация')
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect ('login')

class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url= reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def=self.get_user_context(title = 'обратная связь')
        return dict(list(context.items())+ list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('home')

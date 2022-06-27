from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('', index, name='home'),
    path('',cache_page(60)(WomenHome.as_view()), name='home'),

    path('about/', about, name='about'),
    # path('add_page/', add_page, name='add_page'),
    path('add_page/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),


    path('register/', RegisterUser.as_view(), name='register'),
    # path('post/<slug:post_slug>', read_post, name='read_post'),
    path('post/<slug:post_slug>', ShowPost.as_view(), name='read_post'),
    path('category/<slug:cat_slug>', WomenCategory.as_view(), name='category'),


]

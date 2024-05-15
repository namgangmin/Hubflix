"""
URL configuration for Hubflix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('upload', views.upload_movie, name='upload_movie.html'),
    path('list', views.movie_list, name='movie_list.html'),
   
    path('', views.movie_list2, name='index.html'),
    path('main',  views.main_yl, name='main_yl.html'),
    path('login',  views.login, name='login.html'),
    path('sign_up',  views.signup, name='sign_up.html'),
    path('user_detail',  views.user_detail, name='user_detail.html'),
    path('chatbot',  views.chatbot, name='chatbot.html'),
    path('user_detail_comm',  views.user_detail_comm, name='user_detail_comm.html'),
    path('user_detail_like',  views.user_detail_like, name='user_detail_like.html'),
    path('user_detail_watch',  views.user_detail_watch, name='user_detail_watch.html'),
    path('contents_detail/<int:contents_id>',  views.contents_detail, name='contents_detail.html'),
    path('search',  views.search, name='search.html'),
    path('search_result',  views.search_result, name='search_result.html'),
    path('contents_detail/<int:contents_id>/watching',  views.contents_dw, name='contents_dw.html'),
    path('tv',  views.tv, name='tv.html')
]

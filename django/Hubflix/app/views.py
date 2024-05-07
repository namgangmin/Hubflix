from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.db import connection
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect 
from django.contrib.auth.models import User
from django.contrib import auth
from app.models import Users
from app.serializers import UsersSerializer
from rest_framework import generics

from .forms import MovieForm
from .models import Contents

# Create your views here.
def main_page(request):
    # HTML 파일에 넘겨줄 데이터 정의
    
    
    # HTML 파일에 넘겨줄 추가 내역들 삽입하는 곳
    context = {
        "now": "now"
    } 
    
    # request에 대해 main.html로 context데이터를 넘겨준다.
    return render(request, 'main_page.html', context)


def upload_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm()
    return render(request, 'upload_movie.html', {'form': form})

def movie_list(request):
    movies = Contents.objects.order_by('-popularity')[:8]

    return render(request, 'movie_list.html', {'movies': movies})

def movie_list2(request):
    movies = Contents.objects.order_by('-popularity')[:4]
    movies2 = Contents.objects.order_by('-release_date')[:4]
    movies3 = Contents.objects.order_by('-vote_average')[3:7]
    movies4 = Contents.objects.all()[:4]
    movies5 = Contents.objects.order_by('-release_date')[30:34]

    return render(request, 'index.html', {'movies': movies, 'movies2' : movies2, 
                                          'movies3' : movies3, 'movies4' : movies4, 'movies5' : movies5})

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
                auth.login(request, user)
                # Redirect to a success page.
                #return redirect('index')
                return redirect('./')
        else:
            # Return an 'invalid login' error message.
            return render(request, 'login.html')

class UserCreate(generics.CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
def signup(request):
    if request.method == "POST":
        if request.POST['password']==request.POST['password2']:
            try:
                user = Users.objects.get(username=request.POST['username'])
                return render(request,'sign_up.html',{'error': '이미 존재하는 아이디입니다.'})
            except Users.DoesNotExist:
                user=Users.objects.create_user(
                    user_id=request.POST['user_id'], password=request.POST['password'],
                    email=request.POST['useremail'], name=request.POST['username'], nickname=request.POST['nickname'],
                    birth=request.POST['birth'])
                auth.login(request,user)
                return redirect('./login')
        else:
            return render(request,'sign_up.html')
    return render(request,'sign_up.html')
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.db import connection
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponse 
from django.contrib.auth.models import User
from django.contrib import auth
from app.models import Users
from app.serializers import UsersSerializer
from rest_framework import generics
from datetime import date, timedelta
from django.contrib import messages
import datetime
import re

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
    movies = Contents.objects.filter(release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-release_date')[:4] # 최신 컨텐츠
    movies2 = Contents.objects.filter(vote_count__gte = 50,
                                      release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-vote_average')[:4] # 평점이 높은 컨텐츠
    movies3 = Contents.objects.order_by('-vote_average')[3:7] # 지금 뜨는 컨텐츠
    movies4 = Contents.objects.filter(release_date__gt=date.today()).order_by('release_date')[:4] # 개봉 예정작
    movies5 = Contents.objects.order_by('-release_date')[30:34]

    return render(request, 'index.html', {'movies': movies, 'movies2' : movies2, 
                                          'movies3' : movies3, 'movies4' : movies4, 'movies5' : movies5})

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')

    elif request.method == "POST":
        userid = request.POST.get('user_id', None)
        password = request.POST.get('password', None)
        #user = authenticate(request, username=userid, password=password
        exist_user = Users.objects.filter(user_id = userid)

        if not exist_user:
            messages.add_message(request, messages.ERROR, 'ID가 존재하지 않습니다')
            return render(request, 'login.html')
       
        me = Users.objects.get(user_id = userid)
        context = {}
        if me.password == password:
            request.session['user_id'] = me.user_id
            request.session['nickname'] = me.nickname
            context['user_id'] = request.session['user_id']
            context['nickname'] = request.session['nickname']
            #return render(request, 'main_yl.html',context)
            return redirect('/hubflix/main')
        else:
            messages.add_message(request, messages.ERROR, '비밀번호가 틀렸습니다')
            return redirect('/hubflix/login')
    
        #if user is not None:
        #        auth.login(request, user)
                # Redirect to a success page.
                #return redirect('index')
        #        return redirect('./')
        #else:
        #    # Return an 'invalid login' error message.
        #    return render(request, 'login.html')

class UserCreate(generics.CreateAPIView): ##############
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
def signup(request):
    if request.method == "POST":
        if request.POST['password']==request.POST['password2']: # 비밀번호, 비밀번호 확인 비교
            id = request.POST.get('user_id', None)
            password = request.POST.get('password', None)
            nickname = request.POST.get('nickname', None)
            email = request.POST.get('email', None)
            birth = request.POST.get('birth', None)

            exist_user = Users.objects.filter(user_id = id) # 존재하는 id 인지 비교
            
            if exist_user: # 존재하면 다시 회원가입 창 반환
                messages.add_message(request, messages.ERROR, 'ID가 이미 존재합니다')
                return render (request, 'sign_up.html')
            elif Users.objects.filter(nickname = nickname):
                messages.add_message(request, messages.ERROR, '닉네임이 이미 존재합니다')
                return render (request, 'sign_up.html')
            elif not re.match("^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",email) :
                messages.add_message(request, messages.ERROR, '이메일 형식이 틀렸습니다')
                return render (request, 'sign_up.html')
            elif not datetime.datetime.strptime(birth,"%Y-%m-%d"):
                messages.add_message(request, messages.ERROR, '생일의 날짜 형식이 틀렸습니다')
                return render (request, 'sign_up.html')
            else:
                Users.objects.create(
                user_id = id,
                password = password,
                nickname = nickname,
                email = email,
                birth = birth)
                
                return redirect('./login') # 회원가입 완료
            #try:
            #    user = Users.objects.get(username=request.POST['username'])
            #    return render(request,'sign_up.html',{'error': '이미 존재하는 아이디입니다.'})
            #except Users.DoesNotExist:
            #    user=Users.objects.create_user(
            #        user_id=request.POST['user_id'], password=request.POST['password'],
            #        email=request.POST['useremail'], name=request.POST['username'], nickname=request.POST['nickname'],
            #        birth=request.POST['birth'])
            #    auth.login(request,user)
            #    return redirect('./login')
        else:
            messages.add_message(request, messages.ERROR, '비밀번호가 다릅니다')
            return render (request, 'sign_up.html')
    else:
        return render(request,'sign_up.html')

def main_yl(request):
    movies = Contents.objects.filter(release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-release_date')[:4] # 최신 컨텐츠
    movies2 = Contents.objects.filter(vote_count__gte = 50,
                                      release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-vote_average')[:4] # 평점이 높은 컨텐츠
    movies3 = Contents.objects.order_by('-vote_average')[3:7] # 지금 뜨는 컨텐츠
    movies4 = Contents.objects.filter(release_date__gt=date.today()).order_by('release_date')[:4] # 개봉 예정작
    movies5 = Contents.objects.order_by('-release_date')[30:34]

    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'main_yl.html', {'movies': movies, 'movies2' : movies2, 
                                          'movies3' : movies3, 'movies4' : movies4, 'movies5' : movies5,
                                          'user' : context })

def user_detail(request):
    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'user_detail.html', {'user' : context})


def chatbot(request):
    movies = Contents.objects.order_by('-popularity')[:8]

    return render(request, 'chatbot.html', {'movies': movies})

def user_detail_comm(request):
    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'user_detail_comm.html', {'user' : context})

def user_detail_like(request):
    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'user_detail_like.html', {'user' : context})

def user_detail_watch(request):
    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'user_detail_watch.html', {'user' : context})

def contents_detail(request):
    movies = Contents.objects.order_by('-popularity')[:8]

    return render(request, 'contents_detail.html', {'movies': movies})

def search(request):
    movies = Contents.objects.order_by('-popularity')[:8]

    return render(request, 'search.html', {'movies': movies})

def search_result(request):
    movies = Contents.objects.order_by('-popularity')[:4]

    return render(request, 'search_result.html', {'movies': movies})

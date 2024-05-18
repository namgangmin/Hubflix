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
from django.db.models import Q
import pandas as pd
import numpy as np

from .forms import MovieForm
from .models import Contents
from .models import Ott
from .models import WatchingLog

from datetime import datetime

from .recommend import find_sim_movie

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
    movies = Contents.objects.filter(~Q(overview=""),release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-release_date')[:4] # 최신 컨텐츠
    movies2 = Contents.objects.filter(~Q(overview=""),vote_count__gte = 50,
                                      release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-vote_average')[:4] # 평점이 높은 컨텐츠
    movies3 = Contents.objects.filter(~Q(overview="")).order_by('-vote_average')[3:7] # 지금 뜨는 컨텐츠
    movies4 = Contents.objects.filter(~Q(overview=""),release_date__gt=date.today()).order_by('release_date')[:4] # 개봉 예정작
    movies5 = Contents.objects.filter(~Q(overview="")).order_by('-release_date')[30:34]

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
    movies = Contents.objects.filter(~Q(overview=""),release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-release_date')[:4] # 최신 컨텐츠
    movies2 = Contents.objects.filter(~Q(overview=""),vote_count__gte = 50,
                                      release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-vote_average')[:4] # 평점이 높은 컨텐츠
    movies3 = Contents.objects.filter(~Q(overview="")).order_by('-popularity')[:4] # 지금 뜨는 컨텐츠
    movies4 = Contents.objects.filter(~Q(overview=""),release_date__gt=date.today()).order_by('release_date')[:4] # 개봉 예정작
    
    exist = WatchingLog.objects.filter(user_id = request.session['user_id'])
    
    if exist:
        stitle = WatchingLog.objects.filter(user_id = request.session['user_id']).order_by('-time')[:1].values('contents_title')
        stitles = stitle[0]['contents_title']
        similar_movies = list(find_sim_movie(stitles,6)['title'])
        print(similar_movies)
    else :
        stitle = Contents.objects.filter(vote_count__gte=50,release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-popularity')[:1].values('title')
        stitles = stitle[0]['title']
        print(stitles)
        similar_movies = list(find_sim_movie(stitles,6)['title'])
    
    movies5 = Contents.objects.filter(~Q(overview=""),title = similar_movies[0]).order_by('-release_date')
    for i in range(1,5):
        movie =Contents.objects.filter(~Q(overview=""),title = similar_movies[i]).order_by('-release_date')
        movies5 = movies5 | movie
    print(movies5)
    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'main_yl.html', {'movies': movies, 'movies2' : movies2, 
                                          'movies3' : movies3, 'movies4' : movies4, 'movies5' : movies5,
                                          'user' : context})

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

def contents_detail(request, contents_id):
    movies = Contents.objects.get(contents_id = contents_id)

    user_ids = request.session['user_id']
    user = Users.objects.get(user_id = user_ids).user_id
    print(user)
    content_title = movies.title
    contents_id = contents_id
    WatchingLog.objects.create(
        user_id = user,
        contents_title = content_title,
        contents_id = contents_id,
        time = datetime.now()
    #    id = user
    )

    return render(request, 'contents_detail.html', {'movies': movies, 'contents_id' : contents_id})

def search(request):
    if request.method == "POST":
        search_r = request.POST.get('want')

        return redirect('../hubflix/search_result/'+search_r)

    else:
        return render(request, 'search.html',{'sear' : '쿵푸'})

def search_result(request, title):
    movies = Contents.objects.all().filter(title__contains=title)[:4]
    movies2 = Contents.objects.all().filter(title__contains=title)[4:8]
    movies3 = Contents.objects.all().filter(title__contains=title)[8:12]
    if request.method == "POST":
        search_r = request.POST.get('want')
        return redirect('../search_result/'+search_r)

    return render(request, 'search_result.html', {'movies': movies, 'movies2' : movies2, 'movies3' : movies3, 'title': title})

def contents_dw(request, contents_id):
    movies = Contents.objects.get(contents_id=contents_id)
    haveott = Contents.objects.filter(contents_id=contents_id).values('rent','buy','flatrate')
    ott_df = pd.DataFrame(haveott)

    
    
    ott_df['rent'] = ott_df['rent'].str.split(',')
    ott_df['buy'] = ott_df['buy'].str.split(',')
    ott_df['flatrate'] = ott_df['flatrate'].str.split(',')
    
    rentlen = len(ott_df['rent'][0])
    buylen = len(ott_df['buy'][0])
    flatratelen = len(ott_df['flatrate'][0])

    def ott (a, b):
        c = []
        for i in range(a):
            o = Ott.objects.filter(ott_name__contains=b.str[i][0])
            if o :
                c.append(Ott.objects.get(ott_name__contains=b.str[i][0]))
        return c

    rents = ott(rentlen, ott_df['rent'])
    buys = ott(buylen, ott_df['buy'])
    flatrates = ott(flatratelen, ott_df['flatrate'])
    print(rents)
    

    #ott = {
    #    'rent' : ott_df['rent'],
    #    'buy' : ott_df['buy'],
    #    'flatrate' : ott_df['flatrate']
    #}
    
    #ott = Ott.objects.get(ott_name=ott_df)

    return render(request, 'contents_dw.html', {'movies': movies, 'contents_id' : contents_id, 
                                                'buys' : buys,'rents' : rents,
                                                'flatrates' : flatrates})

def tv(request):
    movies = Contents.objects.filter(~Q(overview=""),type='tv',release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-release_date')[:4] # 최신 컨텐츠
    movies2 = Contents.objects.filter(~Q(overview=""),type='tv',vote_count__gte = 50,
                                      release_date__range=[date.today()-timedelta(days=3600), date.today()]).order_by('-vote_average')[:4] # 평점이 높은 컨텐츠
    movies3 = Contents.objects.filter(~Q(overview=""),type='tv').order_by('-vote_average')[3:7] # 지금 뜨는 컨텐츠
    movies4 = Contents.objects.filter(~Q(overview=""),type='tv')[:4] 
    movies5 = Contents.objects.filter(~Q(overview=""),type='tv').order_by('-release_date')[0:4]

    context = {}
    context['user_id'] = request.session['user_id']
    context['nickname'] = request.session['nickname']

    return render(request, 'tv.html', {'movies': movies, 'movies2' : movies2, 
                                          'movies3' : movies3, 'movies4' : movies4, 'movies5' : movies5, 'user' : context})

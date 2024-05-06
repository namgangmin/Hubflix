from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.db import connection

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
    movies = Contents.objects.order_by('popularity')[:4]

    return render(request, 'index.html', {'movies': movies})

def login(request):
    movies = Contents.objects.order_by('popularity')[:4]

    return render(request, 'login.html', {'movies': movies})

def sign_up(request):
    movies = Contents.objects.order_by('popularity')[:4]

    return render(request, 'sign_up.html', {'movies': movies})
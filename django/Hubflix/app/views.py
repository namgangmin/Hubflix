from django.shortcuts import render
import datetime

# Create your views here.
def main_page(request):
    # HTML 파일에 넘겨줄 데이터 정의
    
    
    # HTML 파일에 넘겨줄 추가 내역들 삽입하는 곳
    context = {
        "now": "now"
    } 
    
    # request에 대해 main.html로 context데이터를 넘겨준다.
    return render(request, 'main_page.html', context)
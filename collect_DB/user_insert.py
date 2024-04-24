import json
import numpy as np
import random
import calendar
from datetime import date, timedelta

# 결과를 JSON형식으로 담을 리스트
user_list = []

def get_rand_name(): # 랜덤 이름 생성
    last_names = ["김", "이", "박", "최", "정", "강", "조", "윤", "장", "임", 
                  "한", "오", "서", "신", "권", "황", "안", "송", "류", "전", 
                  "홍", "고", "문", "양", "손", "배", "조", "백", "허", "유", 
                  "남", "심", "노", "정", "하", "곽", "성", "차", "주", "우",
                  "남궁", "황보", "제갈", "사공", "선우", "서문", "독고"]

    first_names = ["강", "건", "경", "고", "관", "나", "남", "노", "누", "다",
                   "단", "담", "대", "덕", "도", "동", "라", "래", "로", "루", 
                   "마", "만", "명", "무", "문", "미", "민", "백", "범", "별", 
                   "병", "보", "빛", "사", "산", "상", "새", "서", "석", "선", 
                   "아", "안", "애", "엄", "영", "예", "오", "옥", "완", "요", 
                   "자", "장", "재", "전", "정", "조", "종", "주", "준", "지", 
                   "찬", "창", "채", "천", "철", "초", "춘", "복", "치", "탐", 
                   "태", "택", "하", "한", "해", "혁", "현", "형", "혜", "호"]
    
    last_name = random.choice(last_names) # Last name 생성
    first_name = "".join(random.sample(first_names, 2)) # First name 생성     
    full_name = last_name + first_name # Full name 생성
    
    return full_name

def get_rand_phone_number(): # 랜덤 전화번호 생성
    numbers = "0123456789"
    num1 = "".join(random.sample(numbers, 4))
    num2 = "".join(random.sample(numbers, 4))
    
    phone_num = "010-{0}-{1}".format(num1, num2)
    
    return phone_num

def get_rand_email(): # 랜덤 이메일 생성
    alphabet_numbes = "abcdefghizklmnopqrstuvwxyz0123456789"
    domains = ['naver.com', 'kakao.com', 'gmail.com']
    digit = random.randint(4,10)
    
    while(True):
        userid = "".join(random.sample(alphabet_numbes, digit))
        if(userid[0] not in '0123456789'): # 첫 번째 자리가 숫자인지 확인해서
            break
    domain = random.choice(domains)                             # 숫자이면 while문을 빠져나감
    email = f"{userid}@{domain}"
    return email

def get_rand_nickname(): # 랜덤 이름 생성
    last_names = ["예쁜","화난","귀여운","배고픈","철학적인","현학적인","슬픈",
                     "푸른","비싼","밝은"]
    first_names =  ["호랑이","비버","강아지","부엉이","여우","치타","문어",
                   "고양이","미어캣","다람쥐"]
    
    last_name = random.choice(last_names) # Last name 생성
    first_name = random.choice(first_names) # First name 생성     
    full_nickname = last_name +" "+ first_name # Full name 생성
    
    return full_nickname

def randomBirthday(start_year=1901, end_year=2021):
    rand_year = random.randint(start_year, end_year)
    rand_month = random.randint(1, 12)
    rand_date = random.randint(1, calendar.monthrange(rand_year, rand_month)[1])
    return str(rand_year).ljust(4, "0") +"-"+ str(rand_month).rjust(2, "0") +"-"+ str(rand_date).rjust(2, "0")


for i in range(20): 

    user_id = "a" + str(i)
    gender = np.random.randint(1,3)
    name = get_rand_name()
    email = get_rand_email()
    phone_number = get_rand_phone_number()
    nickname = get_rand_nickname()
    birth = randomBirthday()

    dict = {"model" : "app.users",
                "pk" : user_id,
                'fields': {
                    "password": 1234,
                    "name" : name,   
                    "email" : email,
                    "phone_number" : phone_number,
                    "nickname": nickname,
                    "gender": gender,
                    "birth" : birth
                }}            
    user_list.append(dict)
        #except:
        #    pass

with open('user_insert.json', "w", encoding='utf-8') as f:

    json.dump(user_list,f, ensure_ascii=False,indent=4)
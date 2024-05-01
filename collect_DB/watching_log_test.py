import requests
import json

# TMDB API 키
api_key = 'f728b799913e9a49c46409571626d786'

#headers = {
#    "accept": "application/json",
#    "Authorization": "Bearer f728b799913e9a49c46409571626d786"
#}

## Movie 모델 데이터 API 요청
# API 결과를 JSON형식으로 담을 리스트
movie_res = []
i = 1
for pageNum in range(1, 5):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={pageNum}'
    print(url)
    response = requests.get(url)
    data = response.json()
    #data = json.loads(response.text)
    for item in data["results"]:
        #try:
        movie_id = item['id']
        #data = json.loads(response.text) 
        url_detail = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR'
        response_sub = requests.get(url_detail)
        movie = response_sub.json()
        
        # movie_result = movie["results"]

        genre = " "

        genres = movie["genres"] # 장르 추가
            # for item in movie:
        for k in genres:
                genre += k["name"] + ","
        genre = genre[:-1]
        
        dict = {"model" : "app.watching_log",
                "pk" : i,
                'fields': {
                    "contents" : movie['id'],
                    "user_link_num" : 1,
                    "contents_title": movie['title'],
                    "genre": genre,
                }}  
        i = i + 1          
        movie_res.append(dict)
            #except:
            #    pass

with open('wathcing_log_test.json', "w", encoding='utf-8') as f:

    json.dump(movie_res,f, ensure_ascii=False,indent=4)
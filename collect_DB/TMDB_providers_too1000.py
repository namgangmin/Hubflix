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

for pageNum in range(1, 50):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={pageNum}'
    print(url)
    response = requests.get(url)
    data = response.json()
    #data = json.loads(response.text)
    for item in data["results"]:
        #try:
        movie_id = item['id']
        url_p = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}&language=ko-KR'
        print(url_p)
        response = requests.get(url_p)
        data_1 = response.json()
        #data = json.loads(response.text)
        
        if "success" in data_1:
             continue
        movie_provider_result = data_1["results"]

        if "KR" in movie_provider_result:
            kr_movie_provider = movie_provider_result["KR"]  
    
            url_detail = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR'
            response_sub = requests.get(url_detail)
            movie = response_sub.json()
        
        # movie_result = movie["results"]

            genre = " "
            rents = " "
            buys = " "
            flatrates = " "
            if "flatrate" in kr_movie_provider:
                flatrate = kr_movie_provider["flatrate"]
                for provider in flatrate:
                    flatrates += provider["provider_name"] + ","
                flatrates = flatrates[:-1] # 마지막을 추가된 ','을 지움
            if "rent" in kr_movie_provider:
                rent = kr_movie_provider["rent"]
                for provider in rent:
                    rents += provider["provider_name"] + ","
                rents = rents[:-1]
            if "buy" in kr_movie_provider:
                buy = kr_movie_provider["buy"]
                for provider in buy:
                    buys += provider["provider_name"] + ","
                buys = buys[:-1]

            genres = movie["genres"] # 장르 추가
            # for item in movie:
            for k in genres:
                    genre += k["name"] + ","
            genre = genre[:-1]

            dict = {"model" : "app.contents",
                    "pk" : movie['id'],
                    'fields': {
                        "title": movie['title'],
                        "type" : "movie",   
                        "characters" : "미상",
                        "seasons_number" : 0,
                        "release_date": movie['release_date'],
                        "overview": movie['overview'],
                        "runtime" : movie['runtime'],
                        "genre": genre,
                        "vote_count" : movie['vote_count'],
                        "adult": movie['adult'],
                        "vote_average" : movie['vote_average'],
                        "poster_path": movie['poster_path'],
                        "rent": rents,
                        "buy": buys,
                        "flatrate": flatrates,
                        "popularity": movie["popularity"]
                    }}            
            movie_res.append(dict)
            #except:
            #    pass

with open('movie_provider_too_1000.json', "w", encoding='utf-8') as f:

    json.dump(movie_res,f, ensure_ascii=False,indent=4)
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
# 인기있는 페이지 순서대로 값을 받아오는 코드
for pageNum in range(1,50):
    url = f'https://api.themoviedb.org/3/movie/popular?api_key={api_key}&language=ko-KR&page={pageNum}'
    print(url)
    response = requests.get(url)
    data = response.json()
    #data = json.loads(response.text)
    for item in data["results"]:
        #try:
        movie_id = item['id']
        url_d = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=ko-KR'
        print(url_d)
        response_d = requests.get(url_d)
        movie = response_d.json()
        url_c = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={api_key}&language=ko-KR'
        
        response_c = requests.get(url_c)
        movie_char = response_c.json()
        
        url_k =  f'https://api.themoviedb.org/3/movie/{movie_id}/keywords?api_key={api_key}&language=ko-KR'
        response_k = requests.get(url_k)
        movie_keyword = response_k.json() 

        url_p = f'https://api.themoviedb.org/3/movie/{movie_id}/watch/providers?api_key={api_key}&language=ko-KR'
        response_p = requests.get(url_p)
        movie_provider = response_p.json()

        rents = ""
        buys = ""
        flatrates = ""

        if "success" in movie_provider:
             continue
        movie_provider_result = movie_provider["results"]
        if "KR" in movie_provider_result:
            kr_movie_provider = movie_provider_result["KR"]

            if "flatrate" in kr_movie_provider:
                flatrate = kr_movie_provider["flatrate"]
                for provider in flatrate:
                    flatrates += provider["provider_name"] + ","
                flatrates = flatrates[:-1] # 마지막을 추가된 ','을 지움
            else :
                flatrates = "한국에서 지원하는 OTT서비스 없음"
            if "rent" in kr_movie_provider:
                rent = kr_movie_provider["rent"]
                for provider in rent:
                    rents += provider["provider_name"] + ","
                rents = rents[:-1]
            else :
                rents = "한국에서 지원하는 OTT서비스 없음"
            if "buy" in kr_movie_provider:
                buy = kr_movie_provider["buy"]
                for provider in buy:
                    buys += provider["provider_name"] + ","
                buys = buys[:-1]
            else :
                buys = "한국에서 지원하는 OTT서비스 없음"
        else :
            flatrates = "한국에서 지원하는 OTT서비스 없음"
            rents = "한국에서 지원하는 OTT서비스 없음"
            buys = "한국에서 지원하는 OTT서비스 없음"

        #data = json.loads(response.text)
        
        # movie_result = movie["results"]

        genre = ""
        genres = movie["genres"] # 장르 추가
        for k in genres:
                genre += k["name"] + ","
        genre = genre[:-1]

        actor = ""
        actors = movie_char["cast"] # 등장인물 추가
        for k in actors:
            actor += k["name"] + ": "
            actor += k["character"] +","
            if k["order"] == 8:
                break
        actor = actor[:-1]
        
        keyword = ""
        keywords = movie_keyword["keywords"] # 키워드 추가
        for k in keywords:
            keyword += k["name"] + ","
        keyword = keyword[:-1]

        dict = {"model" : "app.contents",
                "pk" : movie['id'],
                'fields': {
                    "title": movie['title'],
                    "type" : "movie",   
                    "characters" : actor,
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
                    "popularity": movie["popularity"],
                    "keyword" : keyword
                }}            
        movie_res.append(dict)
            #except:
            #    pass

with open('movie_char_keywo.json', "w", encoding='utf-8') as f:

    json.dump(movie_res,f, ensure_ascii=False,indent=4)
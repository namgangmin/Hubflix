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
            dict = {"model" : "app.contents",
                    "pk" : item['id'],
                    'fields': {
                        "title": item['title'],
                        "type" : "movie",   
                        "production_countries" : "미상",
                        "characters" : "미상",
                        "seasons_number" : 1,
                        "release_date": item['release_date'],
                        "overview": item['overview'],
                        "runtime" : 123,
                        "genre": item['genre_ids'][0],
                        "vote_count" : item['vote_count'],
                        "adult": item['adult'],
                        "vote_average" : item['vote_average'],
                        "poster_path": item['poster_path'],
                        "rent": "test",
                        "buy": "test",
                        "flatrate": "test"
                    }}
            movie_res.append(dict)
        #except:
        #    pass


print(movie_res)

with open('movie_00.json', "w", encoding='utf-8') as f:

    json.dump(movie_res,f, ensure_ascii=False,indent=4)
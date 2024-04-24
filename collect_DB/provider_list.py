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
url = f'https://api.themoviedb.org/3/watch/providers/movie?api_key={api_key}&language=ko-KR'
print(url)
response = requests.get(url)
data = response.json()

for item in data["results"]:
    if "KR" in item["display_priorities"]:
        ottname = item["provider_name"]
        dict = {"model" : "app.ott",
                "pk" : ottname,
                'fields': {
                    "ott_icon": item["logo_path"],
                    "ott_id" : item["provider_id"]

                }}            
        movie_res.append(dict)
            #except:
            #    pass

with open('provider_list.json', "w", encoding='utf-8') as f:

    json.dump(movie_res,f, ensure_ascii=False,indent=4)
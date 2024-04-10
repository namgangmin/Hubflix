import requests
import json

TMDB_API_KEY = "f728b799913e9a49c46409571626d786"

def get_movie_datas():
    total_data = []

    # 1페이지부터 500페이지까지의 데이터를 가져옴.
    for i in range(1, 30):
        request_url = "https://api.themoviedb.org/3/movie/popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()

        for movie in movies["results"]:
            if movie.get('release_date', ''):
                # Movie 모델 필드명에 맞추어 데이터를 저장함.
                data = {
                    'movie_id': movie['contents_id'],
                    'title': movie['title'],
                    'released_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'vote_avg': movie['vote_average'],
                    'overview': movie['overview'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre']
                }

                total_data.append(data)

    json_data = {
        "name": "movie data",
        "data": data
    }

    with open("movie_data.json", "w", encoding="utf-8") as w:
        json.dump(json_data, w, indent="\\t", ensure_ascii=False)

get_movie_datas()
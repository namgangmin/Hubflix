import pymysql
import pandas as pd
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from ast import literal_eval # 문자열 분해시 사용하는 라이브러리
import ast as ast


conn = pymysql.connect(
    host = '13.209.231.102',
    user = 'nnn',
    password = '0000',
    db = 'Hubflix',
    charset = 'utf8'
)

curs = conn.cursor()

sql = "SELECT * from contents"
curs.execute(sql)
wl_table = curs.fetchall()

wl_df = pd.DataFrame(wl_table)
wl_df = wl_df[[0, 1, 6 , 8, 9, 11, 16, 17]] 
wl_df.columns = ['contents_id','title', 'overview', 'genres', 'vote_count', 'vote_average',
                 'popularity', 'keywords', ]
# MySQL 'hubflix' DB의 'contents' 테이블에서 위 컬럼들의 값을 받아와 데이터프레임으로 저장
#print(wl_df)

# pd.set_option('max_colwidth', 100)
# 문자열을 리스트로 변환
#wl_df["genres"] = wl_df['genres'].apply(eval)
def split(x):
    x = x.split(',')
    return x

#for i in range(a):
#    wl_df['keywords'][i] = wl_df['keywords'][i].split(',')
#print(wl_df['keywords'])

wl_df["genres"] = wl_df["genres"].apply(split)
#wl_df['keywords'] = wl_df['keywords'].apply(split)

wl_df['genre_literal'] = wl_df['genres'].apply(lambda x : (' ').join(x))
#wl_df['keywords_literal'] = wl_df['keywords'].apply(lambda x : (' ').join(x))

count_vect = CountVectorizer(min_df=0.0, ngram_range=(1,2))
genre_mat = count_vect.fit_transform(wl_df['genre_literal'])
#keywords_mat = count_vect.fit_transform(wl_df['keywords_literal'])

genre_sim = cosine_similarity(genre_mat, genre_mat)
#keywords_sim = cosine_similarity(keywords_mat, keywords_mat)
# similarity_genre = cosine_similarity(genre_mat, genre_mat).argsort()[:,::-1]
genre_sim_sorted_ind = genre_sim.argsort()[:, ::-1]
#keywords_sim_sorted_ind = keywords_sim.argsort()[:, ::-1]


# 영화의 평점에 따라 필터링해서 최종 추천하는 방식
C = wl_df['vote_average'].mean()
m = wl_df['vote_count'].quantile(0.6)
print('C:',round(C,3), 'm:',round(m,3))

percentile = 0.6
m = wl_df['vote_count'].quantile(percentile)
C = wl_df['vote_average'].mean()
# v : 개별 영화에 평점을 투표한 횟수
# m : 평점을 부여하기 위한 최소 투표 횟수
# R : 개별 영화에 대한 평균 평점.
# C : 전체 영화에 대한 평균 평점
def weighted_vote_average(record,m=m, c=C):
    v = record['vote_count']
    R = record['vote_average']

    return ( (v/(v+m)) * R ) + ( (m/(m+v)) * C )   

wl_df['weighted_vote'] = wl_df.apply(weighted_vote_average, axis=1) 
def find_sim_movie(title_name,top_n=4, sorted_ind = genre_sim_sorted_ind, df = wl_df ):
   
    title_movie = df[df['title'] == title_name]
    title_index = title_movie.index.values
    
    similar_indexes = sorted_ind[title_index, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)

    # 본인제외
    similar_indexes = similar_indexes[similar_indexes != title_index]
    #타겟 영화와 비슷한 코사인유사도값
    # sim_index = genre_sim_sorted_ind[title_index, :top].reshape(-1)
    #본인 제외
    # sim_index = sim_index[sim_index!=title_movie]

    # result = df.iloc[sim_index].sort_values('score',ascending=False)[:10]
    # score 정의 필요

    #return result
    

    return df.iloc[similar_indexes]



import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

with open('boxoffice.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    movieCds = []
    for row in reader:
      movieCds.append(row['movieCd'])

base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.json'
key = config('API_KEY')
movies_info = []


for movieCd in movieCds:

    api_url = f'{base_url}?key={key}&movieCd={movieCd}'
    response = requests.get(api_url)
    data = response.json()
    
    if data['movieInfoResult']['movieInfo']['audits'] == []:
        pass
    else:
        watchGradeNm = data['movieInfoResult']['movieInfo']['audits'][0]['watchGradeNm']
    
    if data['movieInfoResult']['movieInfo']['genres'] == []:
        pass
    else:
        genreNm = data['movieInfoResult']['movieInfo']['genres'][0]['genreNm']
    
    if data['movieInfoResult']['movieInfo']['directors'] == []:
        pass
    else:
       directors = data['movieInfoResult']['movieInfo']['directors'][0]['peopleNm']
    
    temp = {
            'movieCd' : movieCd,
            'movieNm' : data['movieInfoResult']['movieInfo']['movieNm'],
            'movieNmEn' : data['movieInfoResult']['movieInfo']['movieNmEn'],
            'movieNmOg' : data['movieInfoResult']['movieInfo']['movieNmOg'],
            'watchGradeNm' : watchGradeNm,
            'openDt': data['movieInfoResult']['movieInfo']['openDt'],
            'showTm' : data['movieInfoResult']['movieInfo']['showTm'],
            'genreNm' : genreNm,
            'directors' : directors,
            }

    movies_info.append(temp)
    temp = {}

# movies_info 는 top_10 이랑 같은 규모
# print(movies_info)

with open('movie2.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 저장한다.
    fieldnames = ('movieCd','movieNm','movieNmEn','movieNmOg' ,'watchGradeNm' ,'openDt' ,'showTm' ,'genreNm' ,'directors', ) # 항목별 이름
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader() # 헤더를 생성한다.

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for movie_info in movies_info:
        writer.writerow(movie_info) # 어벤져스라는 딕셔너리 안에 
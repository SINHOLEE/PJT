import requests
from decouple import config
from pprint import pprint
import time
import csv


with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    movive_cd_nm = {row['영화 대표코드'] : [row['영화명(국문)'], row['개봉연도'][:4], row['감독']] for row in reader}


pprint(movive_cd_nm)


# ID = config('CLIENT_ID')
# SECRET = config('CLIENT_SECRET')

# # 헤더정보? 어떤정보?
# BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
# HEADERS = {
#     'X-Naver-Client-id' : ID,
#     'X-Naver-Client-Secret' : SECRET,
# }
# movie_naver = []



# for key, value in movive_cd_nm.items():  # key = 코드번호, value[0] : 영화이름 value[1] 개봉연도 value[2] 감독
#     query = value[0]
#     # API_URL = f'{BASE_URL}?query={query}'
#     # response = requests.get(API_URL, headers=HEADERS).json()

#     # # pprint(response)

#     # query = '비스트'
#     API_URL = f'{BASE_URL}?query={query}'
#     response = requests.get(API_URL, headers=HEADERS).json()
#     dic = {}
#     time.sleep(0.1)
#     # pprint(response.get('items'))
#     # print(key)
#     try:
#         if len(response.get('items')) == 1:
#             mvNm = response.get('items')[0].get('title').replace('<b>','').replace('</b>','')
#             link = response.get('items')[0].get('link')
#             imaurl = response.get('items')[0].get('image')
#             rate = response.get('items')[0].get('userRating')
#             dic = {
#                 'movieCd' : key,
#                 'link' : link,
#                 'imgurl' : imaurl, 
#                 'rate' : rate,
#                 '감독' : [value[2], response.get('items')[0].get('director')],
#                 '연도' : [value[1], response.get('items')[0].get('pubDate')],
#                 '제목' : [query,mvNm],
#                 '비고' : '동명영화 없음',
#             }
#             print('1개', query)  # 디버그용
#             movie_naver.append(dic)
#             print(dic)
            
#         else:
#             print('이상 1개', query)  # 디버그용
#             switch = 0
#             for i in range(len(response.get('items'))):
#                 mvNm = response.get('items')[i].get('title').replace('<b>','').replace('</b>','')
#                 # print(response.get('items')[i].get('director')[:-1] , value[2])  # 디버그용
#                 if mvNm == query :
#                     link = response.get('items')[i].get('link')
#                     imaurl = response.get('items')[i].get('image')
#                     rate = response.get('items')[i].get('userRating')
#                     if len(imaurl) == 0:
#                         imaurl = ''
#                     dic = {
#                             'movieCd' : key,
#                             'link' : link,
#                             'imgurl' : imaurl , 
#                             'rate' : rate,
#                             '감독' : [value[2],response.get('items')[i].get('director')[:-1]],
#                             '연도' : [value[1], response.get('items')[i].get('pubDate')],
#                             '제목' : [query,mvNm],
#                             '비고' : 'fit'
#                         }
#                     print(dic,"i =", i )
#                     print(str(response.get('items')[i].get('director')[:-1]) in str(value[2]))
#                     movie_naver.append(dic)
#                     break
#                 #     switch = 1
#                 # else:
#                 #     mvNm = response.get('items')[0].get('title').replace('<b>','').replace('</b>','')
#                 #     link = response.get('items')[0].get('link')
#                 #     imaurl = response.get('items')[0].get('image')
#                 #     rate = response.get('items')[0].get('userRating')
#                 #     if len(imaurl) == 0:
#                 #         imaurl = ''
#                 #     dic = {
#                 #         'movieCd' : key,
#                 #         'link' : link,
#                 #         'imgurl' : imaurl , 
#                 #         'rate' : rate,
#                 #         '감독' : [value[2],response.get('items')[0].get('director')[:-1]],
#                 #         '연도' : [value[1], response.get('items')[0].get('pubDate')],
#                 #         '제목' : [query,mvNm],
#                 #         '비고' : '동명영화 다를 가능성 있음'
#                 #     }
#                 #     print(dic,"i =", i )
#                 #     movie_naver.append(dic)
#                 #     break


#     except Exception as te:
#         print(te, query)

# # print(movie_naver)
# # pprint(len(response.get('items')))

# with open('movie_naver.csv', 'w', newline='', encoding='utf-8') as f:
#     # 저장할 필드의 이름을 미리 저장한다.
#     fieldnames = ('movieCd','link','imgurl', 'rate',  '감독', '연도', '제목', '비고' ) # 항목별 이름
#     writer = csv.DictWriter(f, fieldnames=fieldnames)

#     # 필드 이름을 csv 파일 최상단에 작성한다.
#     writer.writeheader() # 헤더를 생성한다.

#     # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
#     for code in movie_naver:
#         writer.writerow(code) # 어벤져스라는 딕셔너리 안에 

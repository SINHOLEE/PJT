# PJT_02 파이썬을 활용한 데이터 수집2

## 1. 영화 평점 및 영화 포스터 URL 가져오기

### 하나. 기본 API사용 환경 설정

```python
import requests
from pprint import pprint
CLIENT_ID = '0HdZs0y43Jl__eptw7R1'
CLIENT_SECRET = '9zmEAyD8Wz'

# 헤더정보? 어떤정보?
BASE_URL = 'https://openapi.naver.com/v1/search/movie.json'
HEADER = {
    'X-Naver-Client-id' : CLIENT_ID,
    'X-Naver-Client-Scret' : CLIENT_SECRET,
}

query = '자전차왕 엄복동'
API_URL = f'{BASE_URL}?query={query}'
response = requests.get(API_URL).json()

pprint(response)
```

다음과 작성하여 일단 작동하는지 판단해본다.

```python
 python naver_movie.py
{'errorCode': '024',
 'errorMessage': 'Not Exist Client ID : Authentication failed. (인증에 실패했습니다.)'}
(3.7.4)
```

오류가 발생했다. 왜? headers를 받아오지 않아서...

다음과 같은 코드로 headers를 받아온다.

```python
response = requests.get(API_URL, headers=HEADERS).json()

```

결과물은 다음과 같이 출력된다.

```python
{'display': 1,
 'items': [{'actor': '비|강소라|이범수|',
            'director': '김유성|',
            'image': 'https://ssl.pstatic.net/imgmovie/mdi/mit110/1590/159070_P13_114738.jpg',
            'link': 'https://movie.naver.com/movie/bi/mi/basic.nhn?code=159070',
            'pubDate': '2018',
            'subtitle': 'Race to Freedom : Um Bok Dong',
            'title': '<b>자전차왕 엄복동</b>',
            'userRating': '3.84'}],
 'lastBuildDate': 'Fri, 26 Jul 2019 09:51:38 +0900',
 'start': 1,
 'total': 1}
```



클라이언트 아이디와 시크릿을 감추기 위해 환경변수.env에 옮기고 `from decople import config`로 숨긴다.

```python
pip install python-decouple  # 디커플 패키지 다운받는 명령어
```

### 둘. CSV 파일 불러오기

```python
with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    movive_cd_nm = {row['영화 대표코드'] : [row['영화명(국문)'], row['개봉연도'][:4], row['감독']] for row in reader}


```

결과물을 위해서는 영화 대표코드와 국문 영화명만 필요하지만, 네이버API를 이용하여 검색하는 입력값이 영화 코드가 아니라 영화 이름이기 때문에 동명의 영화가 있다고 판단하여 부수적인 비교데이터를 같이 가져왔다.

```python
{'19880001': ['이웃집 토토로', '2001', '미야자키 하야오'],
 '19990220': ['노팅 힐', '1999', '로저 미첼'],
 '20010291': ['해리포터와 마법사의 돌', '2001', '크리스 콜럼버스'],
 '20020222': ['해리포터와 비밀의 방', '2002', '크리스 콜럼버스'],
 '20060347': ['판의 미로 - 오필리아와 세 개의 열쇠', '2006', '길예르모 델 토로'],
 ...
 }
```

### 셋.  for문을 이용하여 모든 케이스 조사하기

```python
for key, value in movive_cd_nm.items():  # key = 코드번호, value[0] : 영화이름 value[1] 개봉연도 value[2] 감독
    query = value[0]
    API_URL = f'{BASE_URL}?query={query}'
    response = requests.get(API_URL, headers=HEADERS).json()
    dic = {}
    time.sleep(0.1)
    try:
        if len(response.get('items')) == 1:
            mvNm = response.get('items')[0].get('title').replace('<b>','').replace('</b>','')
            link = response.get('items')[0].get('link')
            imaurl = response.get('items')[0].get('image')
            rate = response.get('items')[0].get('userRating')
            dic = {
                'movieCd' : key,
                'link' : link,
                'imgurl' : imaurl, 
                'rate' : rate,
                '감독' : [value[2], response.get('items')[0].get('director')],
                '연도' : [value[1], response.get('items')[0].get('pubDate')],
                '제목' : [query,mvNm],
                '비고' : '동명영화 없음',
            }
            print('1개', query)  # 디버그용
            movie_naver.append(dic)
            print(dic)
            
        else:
            print('이상 1개', query)  # 디버그용
            switch = 0
            for i in range(len(response.get('items'))):
                mvNm = response.get('items')[i].get('title').replace('<b>','').replace('</b>','')
                # print(response.get('items')[i].get('director')[:-1] , value[2])  # 디버그용
                if mvNm == query :
                    link = response.get('items')[i].get('link')
                    imaurl = response.get('items')[i].get('image')
                    rate = response.get('items')[i].get('userRating')
                    if len(imaurl) == 0:
                        imaurl = ''
                    dic = {
                            'movieCd' : key,
                            'link' : link,
                            'imgurl' : imaurl , 
                            'rate' : rate,
                            '감독' : [value[2],response.get('items')[i].get('director')[:-1]],
                            '연도' : [value[1], response.get('items')[i].get('pubDate')],
                            '제목' : [query,mvNm],
                            '비고' : 'fit'
                        }
                    print(dic,"i =", i )
                    print(str(response.get('items')[i].get('director')[:-1]) in str(value[2]))
                    movie_naver.append(dic)
                    break

    except Exception as te:
        print(te, query)

```







##  2

```python
import requests

img_url = 'https://ssl.pstatic.net/imgmovie/mdi/mit110/1590/159070_P13_114738.jpg'

# response = requests.get(img_url)  #1 파일을 응답받습니다.



with open('images/test.jpg', 'wb') as f: # wb옵션은 write binary옵션입니다. 이미지파일은 텍스트가 아니므로 응답받을 때 바이너리 형식으로 받아야 합닏.
    #2 파일을 저장받기 위해서는 binary type으로 변환해야 합니다.
    response = requests.get(img_url, stream=True)
    f.write(response) 
```

이렇게 하면 다음과 같은 오류가 뜹니다.



```python
Traceback (most recent call last):
  File "movie_image.py", line 9, in <module>
    with open('images/test.jpg', 'wb') as f: # wb옵션은 write binary옵션입니다. 이미지파일은 텍스트가 아니므로 응답받을 때 바이너리 형식으로 받아야 합닏.
FileNotFoundError: [Errno 2] No such file or directory: 'images/test.jpg'
```

지정한 디렉토리에 images라는 폴더가 없어서 작동안됨

이미지스 폴더를 만들고 다시 실행했을 때에도 작동이 안됨.

```python
raceback (most recent call last):
  File "movie_image.py", line 12, in <module>
    f.write(response)
TypeError: a bytes-like object is required, not 'Response'
```



그 이유는 `f.write(response.content)` 리스폰스 뒤에 컨텐츠라는 어트리뷰트를 선택하지 않아서 발생한 오류입니다.


# PJT. 파이썬을 활용한 데이터 수집 I

## 1. 목표

- **01.py : 최근 50주간 데이터 중에 주간 박스오피스 TOP10데이터를 수집합니다.**

  - 세부 조건

  1. 주간(월~일)까지 기간의 데이터를 조회합니다.
  2. 조회 기간은 총 50주이며, 기준일(마지막 일자)은 2019년 7월 13일입니다.
  3. 다양성 영화/상업 영화를 모두 포함하여야 합니다.
  4. 한국/외국 영화를 모두 포함하여야 합니다.
  5. 모든 상영지역을 포함하여야 합니다.

  - 결과
    수집된 데이터에서 영화 대표코드 , 영화명 , 해당일 누적관객수 를 기록합니다.

- **02.py : 위에서 수집한 영화 대표코드를 활용하여 상세 정보를 수집합니다.**

  - 결과
    영화별로 영화 대표코드 , 영화명(국문) , 영화명(영문) , 영화명(원문) , 관람등급 , 개봉연도 , 상영시간 , 장
    르 , 감독명의 내용을 저장합니다.

    

- **03.py : 위에서 수집한 영화 감독정보를 활용하여 상세 정보를 수집합니다.**

  - 세부 조건
    영화인명 으로 조회합니다.

  - 결과

    영화인 코드 , 영화인명 , 분야 , 필모리스트의 내용을 저장합니다.

## 2. 사용한 API 정보

![1563530434276](C:\Users\student\AppData\Roaming\Typora\typora-user-images\1563530434276.png)

사용한 API 주소는 모두 영화관입장권통합전상망 오픈API에서 사용하였습니다.

출처 : http://www.kobis.or.kr/kobisopenapi/homepg/apiservice/searchServiceInfo.do 

### 01.py에 사용한 API 정보

인터페이스

| 요청 변수 |      값      |                         설명                         |
| :-------: | :----------: | :--------------------------------------------------: |
|    key    | 문자열(필수) |             발급받은키 값을 입력합니다.              |
| targetDt  | 문자열(필수) | 조회하고자 하는 날짜를 yyyymmdd 형식으로 입력합니다. |

응답구조

| 응답 필드 | 값     | 설명                          |
| --------- | ------ | ----------------------------- |
| movieCd   | 문자열 | 영화의 대표코드를 출력합니다. |
| movieNm   | 문자열 | 영화명(국문)을 출력합니다.    |
| openDt    | 문자열 | 영화의 개봉일을 출력합니다.   |

API요청 코드

```python
 http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json

```



## 3. code 정보

**01.py 전체코드**

```python
import requests
from datetime import datetime, timedelta
from decouple import config
import csv

# 날짜변수 지정
cover = {}
for i in range(50):

    targetDt = datetime(2019, 7, 13) - timedelta(weeks = i )
    targetDt = targetDt.strftime('%Y%m%d') # strftime : str특정 포멧으로 바꾸게 해준다.
    print(targetDt)
    key = config('API_KEY')
    weekGb = 0 # 주일 + 주말
    base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json' 
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb={weekGb}'


    response = requests.get(api_url)
    data = response.json()
    
     
    for rank in range(len(data['boxOfficeResult']['weeklyBoxOfficeList'])):
        if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover.keys():
        # if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover[data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd']].keys(): # 코드 번호
            pass
        else:
            cover.update({
            data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] :
                {
                'movieCd' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'],   
                'movieNm' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieNm'],
                'audiAcc' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['audiAcc'],
                }
            })
top_10 = []


for key in cover.keys():
    top_10.append(cover[key])
print(top_10)


with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 저장한다.
    fieldnames = ('movieCd','movieNm','audiAcc') # 항목별 이름
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader() # 헤더를 생성한다.

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for code in top_10:
        writer.writerow(code) # 어벤져스라는 딕셔너리 안에 

```

**02.py 전체코드**

```python
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
```

**03.py 전체코드**

~~~python
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config
import csv

with open('movie.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    directors_code = {}
    for row in reader:
        if row['directors'] in directors_code.keys():
            pass
        else:
            directors_code.update({row['directors']: row['movieNm']})

directors = []
print(len(directors_code))
aaz = set(directors_code)
aaz = list(aaz)
print(len(aaz))

for director_code in directors_code:

    base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json'
    key = config('API_KEY')
    peopleNm = director_code[0]
    filmoNames = director_code[1]
    api_url = f'{base_url}?key={key}&peopleNm={peopleNm}&filmoNames={filmoNames}'
    


    response = requests.get(api_url)
    data = response.json()
    print(data)
    if data["peopleListResult"]["peopleList"] == []:
        pass
    else:

        if data["peopleListResult"]["peopleList"][0]['repRoleNm'] == '감독':
            temp = {
                "peopleCd" : data["peopleListResult"]["peopleList"][0]['peopleCd'],
                'peopleNm' : data["peopleListResult"]["peopleList"][0]['peopleNm'],
                'repRoleNm' : data["peopleListResult"]["peopleList"][0]['repRoleNm'],
                'filmoNames' : data["peopleListResult"]["peopleList"][0]['filmoNames'],
            }
            directors.append(temp)
        else:
            pass
        
        temp = {}

print(directors) #top


with open('director.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 저장한다.
    fieldnames = ("peopleCd",'peopleNm','repRoleNm','filmoNames' ) # 항목별 이름
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader() # 헤더를 생성한다.

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for director in directors:
        writer.writerow(director) # 어벤져스라는 딕셔너리 안에 
~~~

### 01.py code 상세정보

#### 날짜변수 지정

```python
import requests
from datetime import datetime, timedelta
from decouple import config

cover = {}
for i in range(50):

    targetDt = datetime(2019, 7, 13) - timedelta(weeks = i ) # 여기서부터 2주를 빼겟다.
    targetDt = targetDt.strftime('%Y%m%d') # strftime : str특정 포멧으로 바꾸게 해준다.
    print(targetDt)
    key = config('API_KEY')
    weekGb = 0 # 주일 + 주말
    base_url ='http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.json' 
    api_url = f'{base_url}?key={key}&targetDt={targetDt}&weekGb={weekGb}'


    response = requests.get(api_url)
    data = response.json()
print(data)
```

- 목표는 2019년 7월 13일부터 최근 50주 간의 영화 상세정보를 받아와 boxoffice.csv파일을 생성하고movieCd, movieNm, audiAcc의 데이터만 받아오는 것 입니다.
- 매 주마다의 정보가 필요하므로 datetime모듈의 timedelta메소드를 사용했습니다.
- 부여받은 API는 환경변수 (.env)에 API_KEY라는 이름으로 변수를 지정하였고 decouple모듈의 config메소드를 사용하여 개인정보를 보호하였습니다.
- .env 에 저장된 API_KEY값을 github에 올리지 않기 위해 .gitignore 파일을 생성하여 그 안에 .env를 지정합니다.
- requests 메소드를 사용하여 받아온 데이터는 다음과 같은 형식입니다.

#### 받아온 데이터의 형태

```python
{'boxOfficeResult': 
	{'boxofficeType': '주간 박스오피스', 
	'showRange': '20190708~20190714', 
	'yearWeekTime': '201928', 
	'weeklyBoxOfficeList': [
		{
		'rnum': '1', 
		'rank': '1', 
		'rankInten': '0', 
		'rankOldAndNew': 'OLD', 
		'movieCd': '20196309', 
		'movieNm': '스파이더맨: 파 프롬 홈', 
		'openDt': '2019-07-02', 
		'salesAmt': '18704459230', 
		'salesShare': '50.6', 
		'salesInten': '-20291831880', 
		'salesChange': '-52.0', 
		'salesAcc': '57709310340', 
		'audiCnt': '2163519', 
		'audiInten': '-2357242', 
		'audiChange': '-52.1', 
		'audiAcc': '6685136', 
		'scrnCnt': '1900', 
		'showCnt': '61772'
		}, 
		{
		'rnum': '2', 
		'rank': '2', 
		'rankInten': '0', 
		'rankOldAndNew': 
		'OLD', 'movieCd': 
		'20183867', 
		'movieNm': '알라딘', 
		'openDt': '2019-05-23', 
		'salesAmt': '8048707260', 
		'salesShare': '21.8', 
		'salesInten': '-370620', 
		'salesChange': '0.0', 
		'salesAcc': '86703864479', 
		'audiCnt': '938604', 
		'audiInten': '-12271', 
		'audiChange': '-1.3', 
		'audiAcc': '10161238', 
		'scrnCnt': '975', 
		'showCnt': '20260'
		}, 
		... ...
```

- 우리가 필요한 정보는 `data['boxOfficeResult']['weeklyBoxOfficeList']` 안에 있는 dictionary 형식의 

데이터 중 영화의 대표코드, 영화 제목, 누적관객 수 입니다.

#### TOP 10데이터 한 곳에 모아 받기

```python
  for rank in range(len(data['boxOfficeResult']['weeklyBoxOfficeList'])):
        if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover.keys():
            pass
        else:
            cover.update({
            data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] :
                {
                'movieCd' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'],   
                'movieNm' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieNm'],
                'audiAcc' : data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['audiAcc'],
                }
            })
```

- 처음에는 큰 리스트 안에 3 가지 정보(영화의 대표코드, 영화 제목, 누적관객 수)를 한 번에 담아논 작은 리스트를 모아 2차원 리스트를 구성하는 방식으로 접근하였습니다. 하지만 이러한 방법은 리스트의 index로만 접근할 수 있기 때문에 movieCd를 직접 검색하여 원하는 자료에 접근할 수 없었습니다. 이러한 문제점을 해결하기 위해 **<u>Dictionary구조의 cover 데이터</u>**를 구성하였습니다.

```python
cover = {
	'20196309': {'movieCd': '20196309', 
        		'movieNm': '스파이더맨: 파 프롬 홈', 
        		'audiAcc': '6685136'}, 
    '20183867': {'movieCd': '20183867', 
                 'movieNm': '알라딘', 
                 'audiAcc': '10161238'}, 
    '20184047': {'movieCd': '20184047', 
                 'movieNm': '토이 스토리 4', 
                 'audiAcc': '3151062'}, 
    '20185353': {'movieCd': '20185353', 
                 'movieNm': '기방도령', 
                 'audiAcc': '220182'}, 
    '20183782': {'movieCd': '20183782', 
                 'movieNm': '기생충', 
                 'audiAcc': '9919835'}, 
    '20185986': {'movieCd': '20185986', 
                 'movieNm': '진범', 
                 'audiAcc': '106756'}, 
    '20191601': {'movieCd': '20191601', 
                 'movieNm': '극장판 엉덩이 탐정: 화려한 사건 수첩', 
                 'audiAcc': '101245'}, 
    '20199951': {'movieCd': '20199951', 
                 'movieNm': '애나벨 집으로', 
                 'audiAcc': '459037'}, 
    '20196655': {'movieCd': '20196655', 
                 'movieNm': '존 윅 3: 파라벨룸', 
                 'audiAcc': '913066'}, 
    '20192151': {'movieCd': '20192151', 
                 'movieNm': '미드소마', 
                 'audiAcc': '45707'}
		}
```

- 위와 같은 구조의 장점은 `cover[{영화 대표코드}][{영화제목}]`, `cover[{영화 대표코드}][{누적관객수}]` 와 같은 경로로 접근이 가능하여  리스트의 구조였다면 하지 못했을 비교까지 가능했습니다.
- 실제 예로 위의 cover데이터는 현재 가장 상위에 있는 for문을 한 번 반복했을 때의 결과값입니다. 두번째 for문에서 새로 들어오려고 하는 데이터 중에서 만약 cover데이터 안에 있는 <u>영화 대표 코드</u>와 동일한 데이터가 접근한다면

```python
        if data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] in cover.keys():
            pass
        else:
			 cover.update({
            data['boxOfficeResult']['weeklyBoxOfficeList'][rank]['movieCd'] :
                {
                    ... ...
```

위와 같은 조건문에 의해서 추가되지 않는 결과가 나올 것입니다. for문의 i는 숫자가 커질수록 현재시간보다 멀리 있는 데이터이므로 cover데이터가 이미 가지고 있는 누적관객수가 더 크기때문에 새로들어온 데이터는 의미가 없기 때문에 `pass`하였습니다.

#### CSV파일로 받기 위한 전처리

```python
top_10 = []

print(cover)
for key in cover.keys():
    top_10.append(cover[key])
print(top_10)

```

- with open을 이용하여 csv 파일로 받기 위해 `[{'movieCd': '20192151', 'movieNm': '미드소마',  'audiAcc': '45707'}, {'movieCd': '20196655',  'movieNm': '존 윅 3: 파라벨룸', 'audiAcc': '913066'},`]과 같은 형태의 리스트로 변경하였습니다. 

#### CSV 파일로 저장하기

```python
import csv
with open('boxoffice.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 저장한다.
    fieldnames = ('movieCd','movieNm','audiAcc') # 항목별 이름
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader() # 헤더를 생성한다.

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for code in top_10:
        writer.writerow(code) # 어벤져스라는 딕셔너리 안에 

```

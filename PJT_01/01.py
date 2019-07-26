# pip install reqeusts 를 다운받지 않았다면 한번 설치
import requests
from pprint import pprint
from datetime import datetime, timedelta
from decouple import config

# 날짜변수 지정
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
top_10 = []

# print(cover)
for key in cover.keys():
    top_10.append(cover[key])
print(top_10)

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




# print(weekly_list)


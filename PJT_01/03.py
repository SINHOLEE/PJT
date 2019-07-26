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
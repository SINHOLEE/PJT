import requests
import csv


with open('movie_naver.csv', 'r', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    movive_url = {row['movieCd'] : row['imgurl'] for row in reader}
for key, value in movive_url.items():
    print(key, value)

    try:
        img_url = value

        response = requests.get(img_url)  #1 파일을 응답받습니다.


  
        with open(f'images/{key}.jpg', 'wb') as f: # wb옵션은 write binary옵션입니다. 이미지파일은 텍스트가 아니므로 응답받을 때 바이너리 형식으로 받아야 합닏.
            #2 파일을 저장받기 위해서는 binary type으로 변환해야 합니다.
            response = requests.get(img_url, stream=True)
            f.write(response.content) 
    except:
        pass
# csv파일 만드는 연습

avengers = [
    {
        "name": "tony stark",
        "gender": "male",
        "appearances": 3068,
        "years since joining": 52
    },
    {
        "name": "robert bruce banner",
        "gender": "male",
        "appearances": 2089,
        "years since joining": 52
    }
]
import csv
with open('avengers.csv', 'w', newline='', encoding='utf-8') as f:
    # 저장할 필드의 이름을 미리 저장한다.
    fieldnames = ('name', 'gender', 'appearances', 'years since joining') # 항목별 이름
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    # 필드 이름을 csv 파일 최상단에 작성한다.
    writer.writeheader() # 헤더를 생성한다.

    # Dictionary를 순회하며 key값에 맞는 value를 한줄씩 작성한다.
    for avenger in avengers:
        writer.writerow(avenger) # 어벤져스라는 딕셔너리 안에 
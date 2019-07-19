# PJT 가이드라인

1. $ pip install python-decouple

2. 새로만들기 - .env

3. .env 파일 안에 생성

   ```python
   API_KEY='{내가 받은 API KEY주소 입력}' 
   ```

   

4. 01.py 에 다음과 같이 임포트하고 키를 컨피그하여 환경변수에 숨겨논 API키를 불러올 수 있게 설장.

5. ```python
   from decouple import config
   key = config('API_KEY')
   
   ```

6. key = config('API_KEY')

7. git에 올릴때 환경변수를 올리지 않게 하기 위해 .gitignore생성

8. .gitignore안에 다음과 같이 작성 하고 저장

   ```python
   .env
   ```

9. 


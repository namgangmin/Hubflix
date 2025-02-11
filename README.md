# Hubflix
Capstone Design
Dong-Eui University Computer Engineering

[캡스톤디자인 3조 결과보고서 PPT.pptx](https://github.com/user-attachments/files/18746214/3.PPT.pptx)


1. django 프로젝트의 manage.py 파일이 있는 경로로 이동하여 python manage.py runserver를 입력하여 서버를 실행합니다.
2. 새 cmd를 켜고 chatbot/movie/Scripts 경로로 이동하여 activate를 입력합니다. (flask의 가상환경 구동)
3. cd .. 을 두 번 입력하고 flask --debug run을 입력하여 서버를 실행합니다.
4. 127.0.0.1:8000/hublfix/login 을 입력하면 웹페이지 구성의 첫페이지로 이동합니다

   * django을 이용할 가상환경을 만들고 django 프로젝트 실행 시에도 가상환경을 구동하여 실행해야 합니다.
   * 챗봇 사용 시 dialogflow를 이용하기 때문에 google api를 사용하기 위한 google api key를 받아 환경변수로 설정해주어야 합니다. ex) set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\남강민\Desktop\Key\auth\movie-reco-wlx9-a7784a080304.json
   * django와 flask를 실행하기 위한 가상환경에 모두 각 프레임워크를 실행시키기 위한 모듈을 설치해야합니다.

from django.db import models


class Contents(models.Model):
    contents_id = models.CharField(primary_key=True, max_length=100, db_comment='컨텐츠의 고유 ID')
    title = models.CharField(max_length=255, db_comment='컨텐츠의 제목')
    type = models.CharField(max_length=10, db_comment='컨텐츠 타입(시리즈나 드라마 또는 영화)')
    production_countries = models.CharField(max_length=200, db_comment='제작 나라')
    characters = models.CharField(max_length=100, blank=True, null=True, db_comment='등장인물')
    seasons_number = models.IntegerField(blank=True, null=True, db_comment='시즌 수')
    release_date = models.DateField(blank=True, null=True, db_comment='개봉 날짜')
    overview = models.CharField(max_length=300, blank=True, null=True, db_comment='줄거리')
    have_ott = models.IntegerField(blank=True, null=True, db_comment='해당 컨텐츠를 보유한 OTT')
    runtime = models.IntegerField(blank=True, null=True, db_comment='런타임(분)')
    genre = models.CharField(max_length=100)
    vote_count = models.IntegerField(blank=True, null=True)
    adult = models.IntegerField(blank=True, null=True)
    vote_average = models.IntegerField(blank=True, null=True)
    poster_path = models.TextField(blank=True, null=True)
    rent = models.CharField(max_length=100, blank=True, null=True, db_comment='대여')
    buy = models.CharField(max_length=100, blank=True, null=True, db_comment='구매')
    flatrate = models.CharField(max_length=100, blank=True, null=True, db_comment='구독')

    class Meta:
        managed = False
        db_table = 'contents'
        db_table_comment = 'Stores collected content information, 수집한 컨텐츠 정보를 저장하는 테이블'


class HaveOtt(models.Model):
    have_ott_num = models.IntegerField(primary_key=True)
    contents = models.ForeignKey(Contents, models.DO_NOTHING, db_comment='컨텐츠 아이디')
    ott_name = models.ForeignKey('Ott', models.DO_NOTHING, db_column='ott_name', db_comment='OTT 이름')

    class Meta:
        managed = False
        db_table = 'have_ott'
        db_table_comment = 'OTT information contained in content, 컨텐츠가 가지고 있는 OTT 정보'


class Ott(models.Model):
    ott_name = models.CharField(primary_key=True, max_length=100, db_comment='OTT 이름')
    ott_icon = models.TextField(blank=True, null=True, db_comment='OTT 아이콘(이미지)')

    class Meta:
        managed = False
        db_table = 'ott'
        db_table_comment = 'Linkable OTT, 연동이 가능한 OTT'


class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_comment='작성자의 아이디(외래키)')
    title = models.CharField(max_length=45, db_comment='제목')
    contents = models.CharField(max_length=200, db_comment='게시글의 내용')
    time = models.DateField(blank=True, null=True, db_comment='게시한 시간')

    class Meta:
        managed = False
        db_table = 'post'
        db_table_comment = 'Stores post, 게시글을 저장하는 테이블'


class Review(models.Model):
    review_num = models.IntegerField(primary_key=True, db_comment='리뷰의 고유한 번호')
    contents = models.ForeignKey(Contents, models.DO_NOTHING, db_comment='컨텐츠 아이디')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_comment='유저 아이디')
    rating = models.IntegerField(blank=True, null=True, db_comment='평점')
    review_contents = models.CharField(max_length=200, db_comment='리뷰 내용')
    review_time = models.DateField(db_comment='리뷰 시간')

    class Meta:
        managed = False
        db_table = 'review'
        db_table_comment = 'store review information, 리뷰 정보 저장'


class UserLinkInfo(models.Model):
    user_link_num = models.IntegerField(primary_key=True, db_comment='유저 연동 정보의 고유한 번호')
    user = models.ForeignKey('Users', models.DO_NOTHING, db_comment='유저의 ID')
    ott_name = models.ForeignKey(Ott, models.DO_NOTHING, db_column='ott_name', db_comment='연동할 OTT의 이름')
    ott_id = models.CharField(max_length=50, db_comment='연동할 OTT의 ID')
    ott_password = models.CharField(max_length=100, db_comment='연동할 OTT의 비밀번호')
    ott_profile = models.CharField(max_length=45, blank=True, null=True, db_comment='연동할 OTT의 프로필')

    class Meta:
        managed = False
        db_table = 'user_link_info'
        db_table_comment = 'Save user linkage information, 유저 연동 정보를 저장하는 테이블'


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50, db_comment='아이디')
    password = models.CharField(max_length=100, db_comment='비밀번호')
    name = models.CharField(max_length=20, db_comment='이름')
    email = models.CharField(max_length=50, db_comment='이메일')
    phone_number = models.CharField(max_length=50, db_comment='전화번호')
    nickname = models.CharField(max_length=30, db_comment='별명')
    gender = models.IntegerField(db_comment='성별')
    birth = models.CharField(max_length=20, blank=True, null=True, db_comment='생년월일')

    class Meta:
        managed = False
        db_table = 'users'
        db_table_comment = 'Stores collected users information, 수집한 유저의 정보를 저장하는 테이블'
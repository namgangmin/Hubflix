from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, UserManager
from django.contrib.auth.models import BaseUserManager

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Contents(models.Model):
    contents_id = models.IntegerField(primary_key=True, db_comment='컨텐츠의 고유 ID')
    title = models.CharField(max_length=255, db_comment='컨텐츠의 제목')
    type = models.CharField(max_length=10, db_comment='컨텐츠 타입(시리즈나 드라마 또는 영화)')
    characters = models.CharField(max_length=1000, blank=True, null=True, db_comment='등장인물')
    seasons_number = models.IntegerField(blank=True, null=True, db_comment='시즌 수')
    release_date = models.DateField(blank=True, null=True, db_comment='개봉 날짜')
    overview = models.CharField(max_length=5000, blank=True, null=True, db_comment='줄거리')
    runtime = models.IntegerField(blank=True, null=True, db_comment='런타임(분)')
    genre = models.CharField(max_length=100)
    vote_count = models.IntegerField(blank=True, null=True)
    adult = models.IntegerField(blank=True, null=True)
    vote_average = models.IntegerField(blank=True, null=True)
    poster_path = models.CharField(max_length=100, blank=True, null=True)
    rent = models.CharField(max_length=100, blank=True, null=True, db_comment='대여')
    buy = models.CharField(max_length=100, blank=True, null=True, db_comment='구매')
    flatrate = models.CharField(max_length=100, blank=True, null=True, db_comment='구독')
    popularity = models.IntegerField(blank=True, null=True)
    keyword = models.CharField(max_length=1000, blank=True, null=True, db_comment='키워드')

    class Meta:
        managed = False
        db_table = 'contents'
        db_table_comment = 'Stores collected content information, 수집한 컨텐츠 정보를 저장하는 테이블'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Ott(models.Model):
    ott_name = models.CharField(primary_key=True, max_length=100, db_comment='OTT 이름')
    ott_icon = models.TextField(blank=True, null=True, db_comment='OTT 아이콘(이미지)')
    ott_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ott'
        db_table_comment = 'Linkable OTT, 연동이 가능한 OTT'


class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, db_comment='작성자의 아이디(외래키)')
    title = models.CharField(max_length=45, db_comment='제목')
    contents = models.CharField(max_length=200, db_comment='게시글의 내용')
    time = models.DateTimeField(blank=True, null=True, db_comment='게시한 시간')

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
    review_time = models.DateTimeField(db_comment='리뷰 시간')

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


class UserManager(BaseUserManager):
    def create_user(self, user_id, email, name, nickname, birth, password=None):

        if not email:
            raise ValueError("이메일을 입력해주세요")
        if not nickname:
            raise ValueError("닉네임을 입력해주세요")
        if not name:
            raise ValueError("이름을 입력해주세요")
        user = self.model(
            user_id = user_id,
            email=self.normalize_email(email),
            name=name,
            nickname = nickname,
            birth = birth,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, name, password=None):
        user = self.create_user(
            email,
            name=name,
            password=password,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user
    
class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50, db_comment='아이디')
    password = models.CharField(max_length=100, db_comment='비밀번호')
    #username = models.CharField(max_length=20, db_comment='이름',null=False, blank=False)
    email = models.EmailField(verbose_name='email',max_length=50, db_comment='이메일',null=False, blank=False, unique=True)
    #phone_number = models.CharField(verbose_name='email',max_length=50, db_comment='전화번호')
    nickname = models.CharField(max_length=100, db_comment='별명',null=False, blank=False, unique=True)
    #gender = models.IntegerField(db_comment='성별')
    birth = models.DateField(blank=True, null=True, db_comment='생년월일')
    
    ###last_login = models.DateField(blank=True, null=True)
    #first_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    #date_joined = models.DateTimeField()
        
    #is_superuser =models.BooleanField(default=False)
    #is_active = models.BooleanField(default=True)
    # is_admin = models.BooleanField(default=False)

    #objects = UserManager()
   
    USERNAME_FIELD = 'nickname'
    REQUIRED_FIELDS = ['email','nickname']

    #def __str__(self):
    #    return self.nickname
    
    #def has_perm(self,perm,obj=None):
    #    return True
    
    #def has_module_perms(self, app_label):
    #    return True
    
    #@property
    #def is_staff(self):
    #    return self.is_admin

    class Meta:
    #    managed = False
        db_table = 'users'
        db_table_comment = 'Stores collected users information, 수집한 유저의 정보를 저장하는 테이블'


class WatchingLog(models.Model):
    watch_num = models.IntegerField()
    contents = models.ForeignKey(Contents, models.DO_NOTHING, blank=True, null=True)
    user_link_num = models.ForeignKey(UserLinkInfo, models.DO_NOTHING, db_column='user_link_num', blank=True, null=True)
    contents_title = models.CharField(max_length=255, blank=True, null=True)
    genre = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'watching_log'
        db_table_comment = '시청기록'
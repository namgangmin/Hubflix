from django.db import models

# Create your models here.

class Contents(models.Model):
    contents_id = models.CharField(primary_key=True, max_length=100)
    _type = models.CharField(max_length=10)  # '_'로 시작해야함. 이름이 Type라서
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    production_countries = models.CharField(max_length=200)
    seasons_number = models.IntegerField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    summary = models.CharField(max_length=300,blank=True,null=True)
    have_ott = models.IntegerField(blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'contents'


class Users(models.Model):
    user_id = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=100) 
    name = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    nickname = models.CharField(max_length=30)
    gender = models.IntegerField()
    birth = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'


class Post(models.Model):
    post_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column="user_id")
    title = models.CharField(max_length=45)
    contents = models.CharField(max_length=200)
    time = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'

class Ott(models.Model):
    ott_name = models.CharField(primary_key=True, max_length=100)
    ott_icon = models.ImageField(upload_to='uploads/%Y/%m/%d/',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ott'
    
class User_link_info(models.Model):
    user_link_num = models.CharField(primary_key=True, max_length=200)
    user_id = models.ForeignKey(Users, on_delete=models.DO_NOTHING, db_column="user_id")
    ott_name = models.ForeignKey(Ott, on_delete=models.DO_NOTHING, db_column="ott_name")
    ott_id = models.CharField(max_length=50)  # Field renamed because it started with '_'.
    ott_password = models.CharField(max_length=100)
    ott_profile = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'User_link_info'

class Have_ott(models.Model):
    have_ott_num = models.IntegerField(primary_key=True)
    contents_id = models.ForeignKey(Contents, on_delete=models.DO_NOTHING, db_column="contents_id", related_name='+')
    ott_name = models.ForeignKey(Ott, on_delete=models.DO_NOTHING, db_column="ott_name")

    class Meta:
        managed = False
        db_table = 'have_ott'

class Review(models.Model):
    review_num = models.IntegerField(primary_key=True)
    contents_id = models.ForeignKey(Contents, max_length=100, on_delete=models.DO_NOTHING, db_column='contents_id')
    user_id = models.ForeignKey(Users, max_length=50, on_delete=models.DO_NOTHING, db_column='user_id')
    rating = models.IntegerField(blank=True, null=True)
    review_contents = models.CharField(max_length=200)
    review_time = models.DateField()

    class Meta:
        managed = False
        db_table = 'review'
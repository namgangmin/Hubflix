from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents        # Contents 모델 사용
        fields = '__all__'      # 모든 필드 포함


class UsersSerializer(serializers.ModelSerializer):
    #def create(self, validated_data):
    #    user = Users.objects.create_user(
    #        user_id = validated_data['user_id'],
    #        email = validated_data['email'],
    #        nickname = validated_data['nickname'],
    #        username = validated_data['username'],
    #        password = validated_data['password'],
    #        birth = validated_data['birth']
    #    )
    #    return user
    
    class Meta:
        model = Users    # Users 모델 사용
        fields = '__all__'
        #fields = ['user_id', 'nickname', 'email', 'username', 'password', 'birth']          # 모든 필드 포함

#class UserInfoSerializer(serializers.ModelSerializer):

#    class Meta:
#        model = get_user_model()
#        fields = ('user_id','email','username')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # Post 모델 사용
        fields = '__all__'      # 모든 필드 포함


class OttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ott     # Ott 모델 사용
        fields = '__all__'          # 모든 필드 포함


class UserlinkinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLinkInfo    # UserInterworking 모델 사용
        fields = '__all__'          # 모든 필드 포함


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review     # ContentsReview 모델 사용
        fields = '__all__'      # 모든 필드 포함

class WatchingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchingLog     # WatchingLog 모델 사용
        fields = '__all__'      # 모든 필드 포함


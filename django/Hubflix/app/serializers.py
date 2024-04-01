from rest_framework import serializers
from .models import *


class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contents        # Contents 모델 사용
        fields = '__all__'      # 모든 필드 포함


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users    # ContentsEpisodes 모델 사용
        fields = '__all__'          # 모든 필드 포함


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post  # ContentsReview 모델 사용
        fields = '__all__'      # 모든 필드 포함


class OttSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ott     # ContentsSeasons 모델 사용
        fields = '__all__'          # 모든 필드 포함


class User_link_infoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_link_info    # UserInterworking 모델 사용
        fields = '__all__'          # 모든 필드 포함


class Have_ottSerializer(serializers.ModelSerializer):
    class Meta:
        model = Have_ott           # Users 모델 사용
        fields = '__all__'      # 모든 필드 포함


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review     # WatchingLog 모델 사용
        fields = '__all__'      # 모든 필드 포함


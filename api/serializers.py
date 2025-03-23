from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Survey, Question, UserResponse

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class SurveySerializer(serializers.ModelSerializer):
    question_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
        source='questions'
    )

    class Meta:
        model = Survey
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields='__all__'

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserResponse
        fields='__all__'
        extra_kwargs={"user": {"read_only":True}}
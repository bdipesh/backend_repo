from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        token = Token.objects.create(user=user)
        return user, token
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'timestamp', 'user', 'post']

    def create(self, validated_data):
        comment = Comment.objects.create(user_id=2, **validated_data)
        return comment

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'text', 'timestamp', 'user']

    def create(self, validated_data):
        post = Post.objects.create(user_id=2, **validated_data)
        return post
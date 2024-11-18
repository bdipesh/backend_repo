from rest_framework import viewsets, permissions, status
from rest_framework.pagination import PageNumberPagination
from .models import Post, Comment, User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import PostSerializer, CommentSerializer, UserSerializer, LoginSerializer  
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

class LoginViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    permission_classes = [AllowAny]
    http_method_names = ['post', 'get']

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['users'] = User.objects.all()
        return context

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-timestamp')
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    http_method_names = ['post', 'get']
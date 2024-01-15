from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import auth
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import UserProfile



@api_view(["GET"])
def index(request):
    return Response({"message": "this is the index page for now until something"})


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



@api_view(["POST", "GET"])
def registerUser(request):
    username = request.data.get("username")
    email = request.data.get("email")
    password = request.data.get("password")
    user_img  = request.FILES.get("profileImg")

    new_user = User.objects.create_user(username=username, email=email, password=password)
    new_user.save()

    new_user_profile = UserProfile.objects.create(user=new_user, profile_img=user_img)
    new_user_profile.save()

    if new_user:
        refresh = RefreshToken.for_user(new_user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': new_user.id,
            'username': new_user.username,
            'email': new_user.email,
        }

        return Response({"user has been created": data}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Signup process has failed plz try again'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)
        data = {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
        }

        return Response(data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user_id = request.user.id if request.user else None
    username = request.user.username if request.user else None
    current_user_img = UserProfile.objects.get(user=request.user).profile_img.url

    # This is how you get the bio of the user
    current_users_bio = UserProfile.objects.get(user=request.user).user_bio

    context = {
        "current user user": username,
        "current user profile image": current_user_img,
        "current users id": user_id
    }

    return Response(context)


@api_view(['POST'])
def refresh_token(request):
    refresh = request.data.get('currentUserRefreshToken')
    token = RefreshToken(refresh)

    access_token = token.access_token
    return Response({'access': str(access_token)})

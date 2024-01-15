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
from .models import *
from django.shortcuts import get_object_or_404
from authentication.models import UserProfile

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_new_community(request):
    community_name = request.data.get("community_name")
    header_image = request.FILES.get("header_image")
    user = request.user
    description = request.data.get("description")

    new_community = Community.objects.create(user=user, community_name=community_name, header_image=header_image, description=description)
    new_community.save()

    return Response({"message": "New community has been created"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_communities_on_platform(request):
    all_communities = Community.objects.all().order_by("-date_created")

    communities_array = []

    for single_community in all_communities:
        user_profile = get_object_or_404(UserProfile, user=request.user)
        single_community_data = {
            "id": single_community.id,
            "community_name": single_community.community_name,
            "header_image": single_community.header_image.url,
            "description": single_community.description,
            "user_who_created": user_profile.user.username,
            "user_who_created_profileimg": user_profile.profile_img.url
        }

        communities_array.append(single_community_data)

    return Response(communities_array)


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_community_details(request, community_name):
    current_community = get_object_or_404(Community, community_name=community_name)

    user_profile = get_object_or_404(User, community=current_community)
    single_community_data = {
        "id": current_community.id,
        "community_name": current_community.community_name,
        "header_image": current_community.header_image.url,
        "description": current_community.description,
        "user_who_created": user_profile.username
    }

    return Response(single_community_data)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def post_new_image_to_community(request):
    current_community_name = request.data.get("current_community_name")
    image_caption = request.data.get("image_caption")
    image_file = request.FILES.get("image_file")

    requested_community = get_object_or_404(Community, community_name=current_community_name)

    new_image_post = Post.objects.create(user=request.user, caption=image_caption, image_file=image_file, community=requested_community)
    new_image_post.save()

    return Response({"message": "Your new post was saved to community"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def community_detail_page(request, community_name):
    current_community = get_object_or_404(Community, community_name=community_name)
    community_posts = Post.objects.filter(community=current_community).order_by("-date_posted")

    uploaded_posts = []

    for post in community_posts:
        user_profile = get_object_or_404(UserProfile, user=post.user)
        post_data = {
            "id": post.id,
            "caption": post.caption,
            "community": post.community.community_name,
            "image_file": post.image_file.url,
            "user_who_posted_name": user_profile.user.username,
            "user_who_created_community": current_community.user.username,
            "user_who_uploaded_profileimg": user_profile.profile_img.url
        }

        uploaded_posts.append(post_data) 

    if uploaded_posts:
        return Response(uploaded_posts)
    
    return Response({"message": "There are no posts inside this community"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_admin_user_of_community(request, community_name):
    current_community = get_object_or_404(Community, community_name=community_name)

    community_admin_data = {
        "id": current_community.id,
        "user_who_created_community": current_community.user.username,
    }

    return Response(community_admin_data)
    


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_posts_uploaded(request):
    all_posts = Post.objects.all().order_by("-date_posted")

    all_posts_array = []

    for single_post in all_posts:
        user_profile = get_object_or_404(UserProfile, user=single_post.user)
        single_post_data = {
            "id": single_post.id,
            "caption": single_post.caption,
            "user": single_post.user.username,
            "image_file": single_post.image_file.url,
            "user_who_uploaded_profile_img": user_profile.profile_img.url
        }
        all_posts_array.append(single_post_data)
    return Response(all_posts_array)
        

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def upload_new_image_post(request):
    user = request.user
    caption = request.data.get("caption")
    image_file = request.FILES.get("image_file")

    new_image_post = Post.objects.create(user=user, caption=caption, image_file=image_file)
    new_image_post.save()


    return Response({"message": "New post has been successfully created on your backend"})


@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_all_current_users_posts(request):
    user = request.user
    user_profile_img = UserProfile.objects.get(user=user).profile_img.url

    current_users_posts = Post.objects.filter(user=user).order_by("-date_posted")

    uploaded_posts_array = []

    for post in current_users_posts:
        user_profile = get_object_or_404(UserProfile, user=post.user)
        image_data = {
            "id": post.id,
            "image_caption": post.image_caption,
            "image_file": post.image.url,
            "user": post.user.username,
            "user_who_uploaded_profile": user_profile.profile_img.url if user_profile.profile_img else None,
        }
        uploaded_posts_array.append(image_data)
    
    return Response(uploaded_posts_array)

@api_view(["GET"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_current_users_posts(request):
    posts = Post.objects.filter(user=request.user).order_by("-date_posted")

    user_uploaded_posts_array = []

    for single_post in posts:
        user_who_uploaded_profile = get_object_or_404(UserProfile, user=single_post.user)
        single_post_data = {
            "id": single_post.id,
            "caption": single_post.caption,
            "image_file": single_post.image_file.url,
            "user_who_uploaded_username": user_who_uploaded_profile.user.username,
            "user_who_uploaded_profileimg": user_who_uploaded_profile.profile_img.url
        }
        user_uploaded_posts_array.append(single_post_data)

    return Response(user_uploaded_posts_array)

    
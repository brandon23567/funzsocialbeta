from django.urls import path
from . import views

urlpatterns = [
    path("create_new_community/", views.create_new_community, name="create_new_community"),
    path("community_detail_page/<str:community_name>/", views.community_detail_page, name="community_detail_page"),
    path("get_all_posts_uploaded/", views.get_all_posts_uploaded, name="get_all_posts_uploaded"),
    path("upload_new_image_post/", views.upload_new_image_post, name="upload_new_image_post"),
    path("get_all_current_users_posts/", views.get_all_current_users_posts, name="get_all_current_users_posts"),
    path("get_current_users_posts/", views.get_current_users_posts, name="get_current_users_posts"),
    path("get_all_communities_on_platform/", views.get_all_communities_on_platform, name="get_all_communities_on_platform"),
    path("get_current_community_details/<str:community_name>/", views.get_current_community_details, name="get_current_community_details"),
    path("post_new_image_to_community/", views.post_new_image_to_community, name="post_new_image_to_community"),
    path("get_admin_user_of_community/<str:community_name>/", views.get_admin_user_of_community, name="get_admin_user_of_community"),

]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt import views as jwt_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from authentication.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/base/", include("base.urls")),
    path("api/authentication/", include("authentication.urls")),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

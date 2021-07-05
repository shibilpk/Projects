from django.urls import  re_path
from rest_framework_simplejwt.views import (TokenRefreshView,)
from . import views

app_name = 'authentication'

urlpatterns = [

    re_path(r'^token/$', views.UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    re_path(r'^token/refresh/$', TokenRefreshView.as_view(), name='token_refresh'),

]

from django.urls import include, path
from .views import CustomLoginView, SignUpView
from . import views

urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.HomePageView.as_view(), name='main'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]

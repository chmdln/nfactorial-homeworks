"""
URL configuration for news_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from debug_toolbar.toolbar import debug_toolbar_urls
from news import views
from django.contrib.auth.views import LoginView
from news.forms import UserLoginForm

urlpatterns = [
    path("sign-up/", views.signup, name="signup"),
    path("login/", 
         LoginView.as_view(template_name="news/registration/login.html",authentication_form=UserLoginForm), 
         name="login"
    ),
    path("", include("django.contrib.auth.urls")),
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),
] + debug_toolbar_urls()

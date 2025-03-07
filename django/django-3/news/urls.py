from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('form/', views.news_form, name='news_form'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
]
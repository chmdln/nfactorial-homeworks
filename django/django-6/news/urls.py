from django.urls import path
from . import views


app_name = 'news'
urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('form/', views.news_form, name='news_form'),
    path('<int:news_id>/', views.news_detail, name='news_detail'),
    path('<int:news_id>/edit/', views.news_edit, name='news_edit'),
    path('<int:news_id>/delete/', views.news_delete, name='news_delete'),
    path('<int:news_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    path('api/news/', views.NewsListAPIView.as_view(), name='news_list_api'),
    path('api/news/post/', views.NewsCreateAPIView.as_view(), name='news_post_api'),
    path('api/news/<int:pk>/', views.NewsDetailAPIView.as_view(), name='news_detail_api'),
    path('api/news/<int:pk>/delete/', views.NewsDeleteAPIView.as_view(), name='news_delete_api'),
]


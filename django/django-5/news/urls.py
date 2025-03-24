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
]
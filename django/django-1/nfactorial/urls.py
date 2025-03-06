from django.urls import path
from . import views

urlpatterns = [
    path('', views.hello_nfactorial, name='hello_nfactorial'),
    path('<int:first>/add/<int:second>/', views.two_sum, name='two_sum'),
    path('transform/<str:text>/', views.transform, name='transform'),
    path('check/<str:word>/', views.is_palindrome, name='is_palindrome'),
    path('calc/<int:first>/<str:operation>/<int:second>/', views.calculate, name='calculate'),
]

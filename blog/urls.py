from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path('blogs/', views.blog_list, name='list'),
    path('blog/<slug:slug>/', views.blog_detail, name='detail')
]

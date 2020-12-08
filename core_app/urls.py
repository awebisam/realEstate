from django.urls import path
from . import views

app_name = "core_app"


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('properties/', views.properties, name='list'),
    path('search/', views.properties, name='search'),
    path('post/', views.post_prop, name='post'),
    path("property/<str:slug>/", views.property_detail, name="property"),
    path("inquiry/", views.inquiry, name="inquiry"),
    path("queries/", views.queries, name="queries"),
]

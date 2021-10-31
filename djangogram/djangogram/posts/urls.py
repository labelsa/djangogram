from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    # /posts/
    path('', views.index, name='index'),

    # /posts/create/
    path('create/', views.post_create, name='post_create'),
]

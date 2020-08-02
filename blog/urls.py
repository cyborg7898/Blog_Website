from . import views
from django.urls import path
#app_name='posts'
urlpatterns=[
    path('',views.PostList.as_view(),name='home'),
    #path('<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<post_id>', views.post_detail, name='post_detail'),
    path('postblog',views.postblog, name='postblog'),
    path('like/',views.like_post,name='like-post'),
]
from django.urls import path,include
from blog import views


app_name = 'app'

urlpatterns = [
     path('', views.index, name='index'),
     path('register/', views.register, name='register'),
     path('otp_verify', views.otp_verify, name='otp'),
     path('login/',views.user_login, name='login'),
     path('logout/',views.user_logout, name='logout'),
     
     path('add_profile/',views.user_profile, name='add_profile'),

     path('new_post/',views.CreatePostView.as_view(), name='create_post'),
     path('new_post/<int:pk>',views.PostDetailView.as_view(), name='post_detail'),
     path('post/drafts/',views.DraftListView.as_view(),name='post_draft'),
     path('post/published/',views.PostListView.as_view(),name='post_list'),
     path('publish/<int:pk>/',views.post_publish,name= 'publish'),
     path('update/<int:pk>/',views.PostUpdateView.as_view(),name= 'update'),
     path('delete/<int:pk>/',views.PostDeleteView.as_view(),name= 'delete'),
     path('add_comment/<int:pk>',views.add_comment,name='add_comment'),

]
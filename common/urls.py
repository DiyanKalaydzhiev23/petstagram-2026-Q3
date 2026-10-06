from django.urls import path
from common import views

app_name = 'common'

urlpatterns = [
    path('', views.home_page_view, name='home'),
    path('like/<int:photo_id>/', views.like_functionality_view, name='like'),
    path('comment/<int:photo_id>/', views.add_comment_view, name='comment'),
    path('share/<int:photo_id>/', views.share_functionality, name='share'),
]

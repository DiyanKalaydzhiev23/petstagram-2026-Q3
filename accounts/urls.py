from django.urls import path, include
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('profile/<int:pk>/', include([
        path('', views.profile_details_view, name='details'),
        path('edit/', views.profile_edit_view, name='edit'),
        path('delete/', views.profile_delete_view, name='delete'),
    ])),
]

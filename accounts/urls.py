from django.contrib.auth.views import LogoutView
from django.urls import path, include
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.RegisterAppUserView.as_view(), name='register'),
    path('login/', views.LoginAppUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', include([
        path('', views.ProfileDetailView.as_view(), name='details'),
        path('edit/', views.ProfileUpdateView.as_view(), name='edit'),
        path('delete/', views.profile_delete_view, name='delete'),
    ])),
]

from django.urls import path, include
from photos import views

app_name = 'photos'

urlpatterns = [
    path('add/', views.photo_add_view, name='add'),
    path('<int:pk>/', include([
        path('', views.photo_details_view, name='details'),
        path('edit/', views.photo_edit_view, name='edit'),
    ])),
]

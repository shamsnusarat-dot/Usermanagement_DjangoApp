from django.urls import path
from .views import (
    UserListCreateView, UserDetailView,
    UserListTemplateView, UserCreateTemplateView,
    UserEditTemplateView, UserDeleteTemplateView,
)

urlpatterns = [
    path('', UserListTemplateView.as_view(), name='user-list-template'),
    path('create/', UserCreateTemplateView.as_view(), name='user-create-template'),
    path('<int:pk>/edit/', UserEditTemplateView.as_view(), name='user-edit-template'),
    path('<int:pk>/delete/', UserDeleteTemplateView.as_view(), name='user-delete-template'),

    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

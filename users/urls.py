from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    UserListCreateView, UserDetailView,
    UserListTemplateView, UserCreateTemplateView,
    UserEditTemplateView, UserDeleteTemplateView,
)

urlpatterns = [
    path('', login_required(UserListTemplateView.as_view()), name='user-list-template'),
    path('create/', login_required(UserCreateTemplateView.as_view()), name='user-create-template'),
    path('<int:pk>/edit/', login_required(UserEditTemplateView.as_view()), name='user-edit-template'),
    path('<int:pk>/delete/', login_required(UserDeleteTemplateView.as_view()), name='user-delete-template'),

    path('api/users/', UserListCreateView.as_view(), name='user-list-create'),
    path('api/users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

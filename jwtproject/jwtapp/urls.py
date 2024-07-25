


from django.urls import path
from .views import RegisterView, LoginView, FileView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('upload-file/', FileView.as_view(), name='upload-file'),
    path('users/', UserListView.as_view(), name='user-list'), 
]

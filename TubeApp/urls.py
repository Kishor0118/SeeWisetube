from django.urls import path
from .views import VideoListCreateView, VideoDetailView, UserCreateView, VideoStreamView
from .views import RegisterView, register,user_login,index,VidoePage,upload_video


urlpatterns = [
    path('videos/', VideoListCreateView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('videos/stream/<int:pk>/', VideoStreamView.as_view(), name='video-stream'),
    path('signup/', UserCreateView.as_view(), name='user-signup'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('index/', index, name='index'),
    path('videopage/', VidoePage, name='videopage'),
    path('upload/', upload_video, name='upload'),
    path('videopage/stream/<int:pk>/', VideoStreamView.as_view(), name='video-stream'),
    path('', register, name='home'),

    
]

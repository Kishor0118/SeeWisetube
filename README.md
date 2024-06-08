# SEEWISE TUBE

SEEWISE TUBE is a video streaming application where users can register, upload their videos, and watch videos uploaded by others. 

## Features

- **Sign In**: Securely log in to your account.
- **Sign Up**: Register with your real email for automated email confirmation.
- **Video Upload**: Upload your videos effortlessly.
- **Video Stream**: Stream videos in high quality.
- **Search Option**: Easily search for videos.
- **Admin Panel**: Manage the application through an admin interface.
- **Automated Email Confirmation**: Receive an email confirmation upon registration.

## Getting Started

### Prerequisites

Ensure you have the following prerequisites installed:

- Python (version 3.6 or later)
- Django (version 3.0 or later)
- Other dependencies listed in the `requirements.txt` file

### Installation

1. Clone the repository:
git clone https://github.com/yourusername/seewise-tube.git

2. pip install -r requirements.txt:

3. python manage.py runserver
after the port number enter "/api/" - It'll redirect to home Page

4. Register: Use your real email to register, as an automated email will be sent for confirmation.

5. Sign In: Log in with your registered credentials.

6. Upload Video: Click on 'Upload' to add your video.

7. Watch Videos: Browse and stream videos uploaded by other users.

8. Search: Use the search option to find specific videos.

9. Admin Panel: Admins can access the panel to manage the application.
  Username : admin
  password : kishor

10. Urls
    - path('videos/', VideoListCreateView.as_view(), name='video-list')
    - path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail')
    - path('videos/stream/<int:pk>/', VideoStreamView.as_view(), name='video-stream')
    - path('signup/', UserCreateView.as_view(), name='user-signup')
    - path('api/register/', RegisterView.as_view(), name='api_register')
    - path('register/', register, name='register')
    - path('login/', user_login, name='login')
    - path('index/', index, name='index')
    - path('videopage/', VidoePage, name='videopage')
    - path('upload/', upload_video, name='upload')
    - path('videopage/stream/<int:pk>/', VideoStreamView.as_view(), name='video-stream')
    - path('', register, name='home')

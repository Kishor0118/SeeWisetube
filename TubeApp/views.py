from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Video, User
from .serializers import VideoSerializer, UserSerializer
import cv2
import threading
from rest_framework import status,views
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import VideoForm
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
from django.core.mail import send_mail
from django.conf import settings  

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

class VideoListCreateView(generics.ListCreateAPIView):
    queryset = Video.objects.all().order_by('-id')
    serializer_class = VideoSerializer

def gen(video_path):
    cap = cv2.VideoCapture(video_path)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

class VideoStreamView(generics.RetrieveAPIView):
    def get(self, request, video_id, *args, **kwargs):
        video = get_object_or_404(Video, id=video_id)
        video_path = video.video_file.path
        return StreamingHttpResponse(gen(video_path),
                                     content_type='multipart/x-mixed-replace; boundary=frame')
def send_welcome_email(email):
    subject = 'Welcome New User!'
    message = 'Thank you for SignUP with our Webpage'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        return HttpResponse('Email sent successfully!')
    except Exception as e:
        return HttpResponse(f'Error sending email: {str(e)}')
    
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered')
            else:
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password
                )
                # Send welcome email
                send_welcome_email(email)
                refresh = RefreshToken.for_user(user)
                messages.success(request, 'Account created successfully')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'register.html')

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the homepage or another page after successful login
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'login.html')

@login_required
def VidoePage(request):
    videos = Video.objects.all()
    context = {'videos': videos}
    return render(request, 'videopage.html', context)

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.user = request.user
            video.save()
            return redirect('videopage')  # Make sure 'videopage' is a valid URL name
    else:
        form = VideoForm()
    return render(request, 'upload.html', {'form': form})

@login_required
def index(request):
    return render(request, 'index.html')

def user_logout(request):
    logout(request)
    return redirect('login')



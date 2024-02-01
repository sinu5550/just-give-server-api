from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
# Create your views here.
class UserProfileViewset(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserSerializer

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            current_site = get_current_site(request)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"{request.scheme}://{current_site.domain}/user/active/{uid}/{token}"
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://127.0.0.1:5500/login.html')
    else:
        return redirect('http://127.0.0.1:5500/registration.html')

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(username= username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                print(token)
                print(_)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class UserLogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')

class ReviewViewset(viewsets.ModelViewSet):
    
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({'message': 'Review created successfully.'}, status=status.HTTP_201_CREATED)
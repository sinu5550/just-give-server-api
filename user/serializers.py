from rest_framework import serializers
from . import models
from .models import UserProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = '__all__'
class UserDetailsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    class Meta:
        model = models.User
        fields = ['id','username','email', 'first_name', 'last_name']
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserDetailsSerializer()
    class Meta:
        model = models.UserProfile
        fields = '__all__'
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_serializer = self.fields['user']
        user_instance = instance.user
        user_instance = user_serializer.update(user_instance, user_data)
        
        instance.image = validated_data.get('image', instance.image)
        instance.mobile_no = validated_data.get('mobile_no', instance.mobile_no)
        instance.coins = validated_data.get('coins', instance.coins)
        
        instance.save()
        return instance
        
        

class RegistrationSerializer(serializers.ModelSerializer):
    mobile_no = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'mobile_no', 'email', 'password', 'confirm_password']

    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        mobile_no = self.validated_data['mobile_no']

        if password != password2:
            raise serializers.ValidationError({'error': "Password Doesn't Matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already exists"})
        if models.UserProfile.objects.filter(mobile_no=mobile_no).exists():
            raise serializers.ValidationError({'error': "This mobile number is already in use"})

        user = User(username=username, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_active = False
        user.save()
        models.UserProfile.objects.create(user=user, mobile_no=mobile_no, id = user.id)


        return user
    
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)

class ReviewUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = ['id','image']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Review
        fields = '__all__' 

    
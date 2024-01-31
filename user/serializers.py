from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.UserProfile
        fields = '__all__'

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


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.StringRelatedField(many=False)
    class Meta:
        model = models.Review
        fields = '__all__' 

    
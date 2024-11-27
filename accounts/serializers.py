from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.password_validation import validate_password
from django.conf import settings



class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password], style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('phone', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15, required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    # def validate(self, attrs):
    #     email = attrs.get('email')
    #     password = attrs.get('password')

    #     if email and password:
    #         user = authenticate(request=self.context.get('request'),
    #                             email=email, password=password)

    #         if not user:
    #             msg = 'Unable to login with provided credentials.'
    #             raise serializers.ValidationError(msg, code='authorization')
    #     else:
    #         msg = 'Must include "email" and "password".'
    #         raise serializers.ValidationError(msg, code='authorization')

    #     attrs['user'] = user
    #     return attrs


class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'dob', 'image', 'created_at', 'updated_at', 'updated_at']
        # depth = 1

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            image = obj.image.url
            if request is not None:
                return request.build_absolute_uri(image)
            return f"{settings.BASE_URL}{image}"
        return None
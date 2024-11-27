from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import *
from rest_framework.response import Response
from rest_framework import status
from accounts.utils import *
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'code': status.HTTP_201_CREATED, 'message': 'User registered successfully!'}, status=status.HTTP_201_CREATED)
        return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data.get('phone')
            password = serializer.validated_data.get('password')

            user = authenticate(request, phone=phone, password=password)

            if user is not None:
                login(request, user)
                token = get_user_tokens(user)
                return Response({'status': 'success', 'code': status.HTTP_200_OK, 'message': 'User successfully logged in.', 'tokens': token}, status=status.HTTP_200_OK)
            
        return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        id = request.query_params.get('id')
        user = request.user

        if id and str(id) != str(user.id):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'You can only access your own profile.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile)
            return Response({'status': 'success', 'code': status.HTTP_200_OK, 'data': serializer.data}, status=status.HTTP_200_OK)
        
        except Profile.DoesNotExist:
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, "error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)


    def patch(self, request, *args, **kwargs):
        id = request.query_params.get('id')
        user = request.user

        if id and str(id) != str(user.id):
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': 'You can only edit your own profile.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, "error": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'code': status.HTTP_200_OK, 'message': 'Profile successfully updated!', 'data': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': 'error', 'code': status.HTTP_400_BAD_REQUEST, 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
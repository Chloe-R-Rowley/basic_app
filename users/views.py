# users/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserSerializer, UserProfileSerializer
from django.core.cache import cache

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create UserProfile associated with the user
            UserProfile.objects.create(user=user, mobile_number=request.data['mobile_number'])

            # Serialize user details to send in the response
            user_data = UserProfileSerializer(user.userprofile).data

            # Include additional user details
            user_data.update({
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })

            # Issue access token upon successful registration
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token), 'user': user_data}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            # Serialize user details to send in the response
            user_data = UserProfileSerializer(user.userprofile).data

            # Include additional user details
            user_data.update({
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name
            })

            # Issue access token upon successful login
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token), 'user': user_data})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         if user.is_authenticated:
#             # Blacklist the user's access token
#             access_token = request.auth
#             cache.set(access_token, 'blacklisted', timeout=3600)  # Set a timeout as needed

#             # Logout the user from the Django authentication system
#             logout(request)

#             return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'User not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)


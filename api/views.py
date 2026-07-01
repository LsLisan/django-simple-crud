import json
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from api.serializer import UserSerializer

# 1. PUBLIC VIEW: Anyone can get a user (or keep it dummy as you had it)
@api_view(['GET'])
def get_user(request, user_id):
    dummy_users_database = {
        "1": {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "role": "Admin"},
        "2": {"id": 2, "name": "Bob Jones", "email": "bob@example.com", "role": "User"},
        "3": {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "role": "User"},
    }
    user_id_str = str(user_id)
    if user_id_str in dummy_users_database:
        return Response(dummy_users_database[user_id_str], status=status.HTTP_200_OK)
    return Response({'error': 'User not found (Dummy Data)'}, status=status.HTTP_404_NOT_FOUND)

# 2. PUBLIC VIEW: Let new users register
# 2. PUBLIC VIEW: Let new users register AND return tokens immediately
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # 1. Save the new user to the database
        user = serializer.save()
        
        # 2. Generate JWT tokens for the newly created user object
        refresh = RefreshToken.for_user(user)
        
        # 3. Combine user data and tokens into the final response
        response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered and authenticated successfully!'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. PROTECTED VIEW: Only users with a valid JWT token can see all users
@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 🔒 Locked down with JWT
def get_all_users(request):
    # You can now access the logged-in user via request.user
    print(f"Request made by: {request.user.email}") 
    
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 4. PROTECTED VIEW: Only logged-in users can update or delete
@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])  # 🔒 Locked down with JWT
def update_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)

# 5. SECURE LOGIN: Generates and returns a JWT token pair
@api_view(['POST'])
def login_user(request):
    data = request.data
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format'}, status=status.HTTP_400_BAD_REQUEST)

    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Find user by email
        user = User.objects.get(email=email)
        
        # Check if the password matches using Django's check_password
        if user.check_password(password):
            # Generate JWT tokens for this user
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'message': 'Login successful! Use the access token in Authorization header: Bearer <access_token>'
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
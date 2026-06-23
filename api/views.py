from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User

from api.serializer import UserSerializer
# Commenting these out for now since we aren't using the real DB/Serializer yet
# from .models import User
# from .serializer import UserSerializer

@api_view(['GET'])
def get_user(request, user_id):
    # 1. Create a dictionary of dummy users to simulate a database
    dummy_users_database = {
        "1": {"id": 1, "name": "Alice Smith", "email": "alice@example.com", "role": "Admin"},
        "2": {"id": 2, "name": "Bob Jones", "email": "bob@example.com", "role": "User"},
        "3": {"id": 3, "name": "Charlie Brown", "email": "charlie@example.com", "role": "User"},
    }
    
    user_id_str = str(user_id)
    
    if user_id_str in dummy_users_database:
        return Response(dummy_users_database[user_id_str], status=status.HTTP_200_OK)
    else:
        return Response({'error': 'User not found (Dummy Data)'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH', 'DELETE'])
def update_user(request, user_id):
    if request.method == 'PATCH':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
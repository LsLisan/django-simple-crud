import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Todo, User
from .serializer import TodoSerializer, UserSerializer


@api_view(['GET'])
def api_root(request):
    return JsonResponse({
        'message': 'Welcome to the API',
        'endpoints': [
            '/api/user/create/',
            '/api/login/',
            '/api/all/users/',
            '/api/user/<id>/',
            '/api/tasks/',
        ]
    })


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


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'User registered and authenticated successfully!'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
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
        user = User.objects.get(email=email)
        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data,
                'message': 'Login successful! Use the access token in Authorization header: Bearer <access_token>'
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list_create(request):
    if request.method == 'GET':
        tasks = Todo.objects.filter(owner=request.user)
        serializer = TodoSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    serializer = TodoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(owner=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    try:
        task = Todo.objects.get(id=task_id, owner=request.user)
    except Todo.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        return Response(TodoSerializer(task).data, status=status.HTTP_200_OK)

    if request.method == 'PATCH':
        serializer = TodoSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    task.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
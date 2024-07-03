from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import LoginSerializer, SignupSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import *

@api_view(["POST"])
def login(request, *args, **kwargs):
    serializer = LoginSerializer(data=request.data)
    print(User.objects.get(first_name="admin"))
    if not serializer.is_valid():
        return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                        status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user = User.objects.get(email = serializer.validated_data['email'])
    if user:
        token, created = Token.objects.get_or_create(user=user)
        print(token.user)
        return Response({'data': {'user_token': token.key}}, status=status.HTTP_201_CREATED)
    return Response({"error": {"code": 401, "message": "Login failed"}},
                    status=status.HTTP_401_UNAUTHORIZED)



@api_view(["POST"])
def signup(request, *args, **kwargs):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token = Token.objects.create(user=user)
        return Response({'data': {'user_token': token.key}}, status=status.HTTP_201_CREATED)
    return Response({"error": {"code": 422, "message": "Validation error", "errors": serializer.errors}},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.user.is_active:
        print(1)
        print(1)
        print(1)
        print(1)
        print(1)
        request.user.auth_token.delete()
        return Response({"logout"}, status=status.HTTP_200_OK)
    return Response({"error": {"code": 401, "message": "Login failed"}},
                    status=status.HTTP_401_UNAUTHORIZED)



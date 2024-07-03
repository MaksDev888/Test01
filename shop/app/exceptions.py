from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def handler(exc, context=None):
    if exc.default_code == 'authentication_failed' or exc.default_code == 'not_authenticated':
        return Response({"error": {"code": 401, "message": "Login failed"}}, status=status.HTTP_401_UNAUTHORIZED)
    if exc.default_code == 'permission_denied':
        return Response({"error": {"code": 403, "message": "Forbidden for you"}}, status=status.HTTP_403_FORBIDDEN)
    if exc.default_code == 'not_found':
        return Response({"error": {"code": 404, "message": "Not found"}}, status=status.HTTP_404_NOT_FOUND)

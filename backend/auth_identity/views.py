from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import RegisteredDevice, Session
from .serializers import LoginRequestSerializer, RefreshRequestSerializer, TokenPairSerializer, DeviceSerializer
from .services import AuthService, AuthenticationError


def client_ip(request):
    return request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", "0.0.0.0")).split(",")[0].strip()


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        pair = AuthService().authenticate_password(serializer.validated_data["username"], serializer.validated_data["password"], client_ip(request), request.META.get("HTTP_USER_AGENT", ""))
    except AuthenticationError as exc:
        return Response({"error": "authentication_failed", "detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(TokenPairSerializer(pair).data)


@api_view(["POST"])
@permission_classes([AllowAny])
def refresh(request):
    serializer = RefreshRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        pair = AuthService().rotate_refresh_token(serializer.validated_data["refresh_token"], client_ip(request), request.META.get("HTTP_USER_AGENT", ""))
    except AuthenticationError as exc:
        return Response({"error": "invalid_refresh_token", "detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(TokenPairSerializer(pair).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    Session.objects.filter(user_id=request.user.id, revoked_at__isnull=True).update(revoked_at=__import__("django.utils.timezone").utils.timezone.now())
    return Response(status=status.HTTP_204_NO_CONTENT)


class DeviceViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        devices = RegisteredDevice.objects.filter(user_id=request.user.id, revoked_at__isnull=True).values("id", "name", "platform", "last_seen_at", "created_at")
        return Response(list(devices))

    def create(self, request):
        serializer = DeviceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        import hashlib
        device = RegisteredDevice.objects.create(user_id=request.user.id, name=serializer.validated_data["name"], platform=serializer.validated_data["platform"], fingerprint_hash=hashlib.sha256(serializer.validated_data["fingerprint"].encode()).hexdigest(), push_token_ref=serializer.validated_data.get("push_token", ""))
        return Response({"id": str(device.id), "name": device.name, "platform": device.platform}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["delete"])
    def revoke(self, request, pk=None):
        from django.utils import timezone
        RegisteredDevice.objects.filter(id=pk, user_id=request.user.id).update(revoked_at=timezone.now())
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"status": "ok", "module": "authentication_identity"})

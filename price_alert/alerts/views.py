# alerts/views.py

from django.core.cache import cache
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Alert
from .serializers import AlertSerializer
from .filters import AlertFilter
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = AlertFilter
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Filter alerts by the currently authenticated user
        queryset = Alert.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        # Automatically set the user field to the currently authenticated user
        serializer.save(user=self.request.user)
        # Invalidate the cache for this user's alerts
        cache_key = f"user_alerts_{self.request.user.id}"
        cache.delete(cache_key)

    @action(detail=False, methods=['get'])
    def user_alerts(self, request):
        # Get alerts for the current user
        alerts = self.get_queryset()
        cache_key = f"user_alerts_{request.user.id}"
        # Try to get the alerts from the cache
        alerts = cache.get(cache_key)
        if not alerts:
            # If cache is empty, fetch from the database
            alerts = self.get_queryset()
            # Serialize the alerts
            serializer = self.get_serializer(alerts, many=True)
            alerts_data = serializer.data
            # Store the serialized data in the cache
            cache.set(cache_key, alerts_data, timeout=60 * 5)  # Cache for 5 minutes
        else:
            # If cached, alerts is already serialized
            alerts_data = alerts

        return Response(alerts_data)

        # # Apply filtering and pagination
        # page = self.paginate_queryset(alerts)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)
        #
        # serializer = self.get_serializer(alerts, many=True)
        # return Response(serializer.data)

"""
Views for the contest API.
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Contest
from contest import serializers


class ContestViewSet(viewsets.ModelViewSet):
    """
    Manage contests in the database.
    """
    serializer_class = serializers.ContestDetailSerializer
    queryset = Contest.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.order_by('id')

    def get_serializer_class(self):
        """
        Return appropriate serializer class.
        """
        if self.action == 'list':
            return serializers.ContestSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """
        Create a new contest.
        """
        if not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message='You do not have permission to create contests.'
            )
        serializer.save()

    def perform_update(self, serializer):
        """
        Update a contest.
        """
        if not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message='You do not have permission to update contests.'
            )
        serializer.save()

    def perform_destroy(self, instance):
        """
        Delete a contest.
        """
        if not self.request.user.is_staff:
            self.permission_denied(
                self.request,
                message='You do not have permission to delete contests.'
            )
        instance.delete()

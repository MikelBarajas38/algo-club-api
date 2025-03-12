"""
Serializers for the contest API View.
"""

from rest_framework import serializers

from core.models import Contest


class ContestSerializer(serializers.ModelSerializer):
    """
    Serializer for the contest object.
    """

    class Meta:
        model = Contest
        fields = [
            'id',
            'name',
            'url',
            'platform',
            'platform_id'
        ]
        read_only_fields = ['id']


class ContestDetailSerializer(ContestSerializer):
    """
    Serialize for contest detail view.
    """

    class Meta(ContestSerializer.Meta):
        fields = ContestSerializer.Meta.fields + [
            'description',
            'start_time',
            'end_time',
            'last_updated'
        ]
        read_only_fields = ['id', 'last_updated']

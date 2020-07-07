from rest_framework import serializers
from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Link
        fields = ['id', 'owner', 'url', 'title']

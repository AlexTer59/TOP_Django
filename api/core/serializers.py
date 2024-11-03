from django.utils.timezone import localtime
from rest_framework import serializers
from core.models import *


class TaskNoteSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    note = serializers.CharField(max_length=1024)
    profile = serializers.CharField(source='profile.user.username', read_only=True)
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return localtime(obj.created_at).strftime('%d-%m-%Y %H:%M')

    def get_likes_count(self, obj):
        return obj.note_likes.count()

    def get_is_liked(self, obj):
        profile = self.context['request'].user.profile
        return TaskNoteLike.objects.filter(profile=profile, note=obj).exists()

    def create(self, validated_data):
        return TaskNote.objects.create(**validated_data)
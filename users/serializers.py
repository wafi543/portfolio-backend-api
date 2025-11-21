from rest_framework import serializers
from django.apps import apps


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = apps.get_model('users', 'User')
        fields = ['id', 'full_name', 'first_name', 'last_name', 'email', 'job_title', 'phone_number', 'location']
        read_only_fields = ['id', 'full_name']

    def get_full_name(self, obj):
        return obj.get_full_name()

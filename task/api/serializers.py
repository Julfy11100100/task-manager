from datetime import datetime
from rest_framework import serializers
from .models import Task


class ReadOnlyTasksSerializer(serializers.ModelSerializer):
    """
    Serializer for get methods
    """

    class Meta:
        model = Task
        fields = ['id', 'title', 'text', 'date', 'is_complete']



class WriteOnlyTasksSerializer(serializers.ModelSerializer):
    """
    Serializer for post, put, delete methods
    """

    title = serializers.CharField(max_length=120, min_length=1, required=True)
    text = serializers.CharField(min_length=1, required=True)
    date = serializers.DateField(required=True)

    class Meta:
        model = Task
        fields = ['title', 'text', 'date']

    def validate(self, attrs):
        date = attrs.get('date', None)
        today = datetime.today().date()
        if date < today:
            raise serializers.ValidationError(
                "Date cannot be earlier than today "
            )
        return attrs

    def create(self, validated_data):
        return Task.objects.create(**validated_data)




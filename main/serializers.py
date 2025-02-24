from rest_framework import serializers
from .models import SamDUkf

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
    column_easy = serializers.IntegerField(default=2, min_value=1, required=False)
    column_medium = serializers.IntegerField(default=3, min_value=1, required=False)
    column_murakkab1 = serializers.IntegerField(default=4, min_value=1, required=False)
    column_murakkab2 = serializers.IntegerField(default=5, min_value=1, required=False)
    column_hard = serializers.IntegerField(default=6, min_value=1, required=False)
    num_tickets = serializers.IntegerField(min_value=1, required=True)

    




class SamDUkfSerializer(serializers.ModelSerializer):
    class Meta:
        model = SamDUkf
        fields = '__all__'

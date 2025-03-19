from rest_framework import serializers

from document.models import Documents

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Documents
        fields='__all__'
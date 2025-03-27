from rest_framework import serializers

from document.models import Documents

class DocumentSerializer(serializers.ModelSerializer):
    # user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Documents
        fields='__all__'
        
        
class DocumentListUserSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    
    class Meta:
        model = Documents
        fields= ["id","title","amount","description","sender","user","timestamp"]
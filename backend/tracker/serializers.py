from rest_framework import serializers
from .models import MileageEntry

class MileageEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MileageEntry
        fields = '__all__'  # Include all model fields
        
    miles_driven = serializers.FloatField(required=False)  # Allow automatic calculation
import requests
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .models import MileageEntry
from .serializers import MileageEntrySerializer
from tracker.utils import get_distance_in_miles


# Create your views here.
class MileageEntryViewSet(viewsets.ModelViewSet):
    queryset = MileageEntry.objects.all()  # Retrieve all mileage entries
    serializer_class = MileageEntrySerializer  # Serialize data for the API
    permission_classes = [IsAuthenticated]  # Require authentication
    
    def perform_create(self, serializer):
        instance = serializer.save()
        miles_driven = get_distance_in_miles(instance.start_location, instance.end_location)
        
        # If the API fails to fetch distance, default to 0
        instance.miles_driven = miles_driven if miles_driven is not None else 0
        instance.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetDistanceView(APIView):
    """API endpoint to fetch distance between two locations using Google Maps API."""
    def post(self, request):
        """Handles POST request to fetch driving distance."""
        origin = request.data.get("origin")
        destination = request.data.get("destination")

        if not origin or not destination:
            return Response({"error": "Both origin and destination are required."}, status=status.HTTP_400_BAD_REQUEST)

        miles_driven = get_distance_in_miles(origin, destination)
        if miles_driven is None:
            return Response({"error": "Failed to fetch data from Google Maps API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"distance": f"{miles_driven} miles"}, status=status.HTTP_200_OK)

import requests
import logging
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets
from .models import MileageEntry
from .serializers import MileageEntrySerializer
from tracker.utils import fetch_distance_from_google_maps

logger = logging.getLogger(__name__)


# Create your views here.
class MileageEntryViewSet(viewsets.ModelViewSet):
    
    queryset = MileageEntry.objects.all()  # Retrieve all mileage entries
    serializer_class = MileageEntrySerializer  # Serialize data for the API
    permission_classes = [IsAuthenticated]  # Require authentication
    
    # Fetch distance between two locations
    def perform_create(self, serializer):
        instance = serializer.save()
        distance = fetch_distance_from_google_maps(instance.start_location, instance.end_location)

        if distance is not None :
            instance.miles_driven = distance
            instance.save()
        else:
            logger.warning("Failed to fetch distance for %s -> %s", instance.start_location, instance.end_location)



class GetDistanceView(APIView):
    
    # API endpoint to fetch distance between two locations
    def post(self, request):
        origin = request.data.get("origin")
        destination = request.data.get("destination")

        if not origin or not destination:
            return Response({"error": "Both origin and destination are required."}, status=status.HTTP_400_BAD_REQUEST)

        miles_driven = fetch_distance_from_google_maps(origin, destination)
        if miles_driven is None:
            return Response({"error": "Failed to fetch data from Google Maps API."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"distance": f"{miles_driven} miles"}, status=status.HTTP_200_OK)

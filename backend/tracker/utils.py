import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def fetch_distance_from_google_maps(start_location, end_location):
    """Fetch distance between two locations using Google Maps API."""
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": start_location,
        "destinations": end_location,
        "units": "imperial",
        "key": google_maps_api_key,
    }

    try:
        response = requests.get(base_url, params=params, timeout=5)
        response.raise_for_status()  # Raises an error for HTTP failures (4xx, 5xx)
        data = response.json()

        if "rows" not in data or not data["rows"][0]["elements"]:
            logger.error("Invalid response format from Google Maps API: %s", data)
            return None

        distance_text = data["rows"][0]["elements"][0].get("distance", {}).get("text")
        if not distance_text:
            logger.warning("Google Maps API did not return a distance for %s -> %s", start_location, end_location)
            return None

        return float(distance_text.replace(" mi", ""))
    
    except requests.exceptions.Timeout:
        logger.error("Request to Google Maps API timed out.")
    except requests.exceptions.RequestException as e:
        logger.error("Error while calling Google Maps API: %s", e)
    except (KeyError, ValueError) as e:
        logger.error("Unexpected response structure from Google Maps API: %s", e)
    
    return None

import requests
import logging
from django.conf import settings

def get_distance_in_miles(start_location, end_location):
    google_maps_api_key = settings.GOOGLE_MAPS_API_KEY
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": start_location,
        "destinations": end_location,
        "units": "imperial",  # Get distance in miles
        "key": google_maps_api_key,
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    # Log the response for debugging
    logging.debug(f"Google Maps API Response: {data}")

    if response.status_code == 200 and data.get("rows"):
        try:
            distance_text = data["rows"][0]["elements"][0]["distance"]["text"]
            return float(distance_text.replace(" mi", ""))  # Convert "XX mi" to float
        except (KeyError, ValueError):
            logging.error(f"Error parsing distance from response: {e}")
            return None
    logging.error("Failed to fetch valid data from Google Maps API.")
    return None  # Return None if API call fails

from django.db import models
from tracker.utils import fetch_distance_from_google_maps

# Manually input miles, duration, and locations. 
# Automatically calculates average speed before saving based on the formula: Speed = Distance / Time
class MileageEntry(models.Model):
    date = models.DateField(auto_now_add=True)  # Auto-fill date when created
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    miles_driven = models.FloatField()
    duration = models.FloatField(help_text="Time taken in hours")
    average_speed = models.FloatField(blank=True, null=True, help_text="Speed in mph")
    
    def save(self, *args, **kwargs):
        """Fetch miles_driven from Google Maps API if not manually provided and calculate average speed."""
        if self.miles_driven is None:
            self.miles_driven = fetch_distance_from_google_maps(self.start_location, self.end_location) or 0  # Default to 0 if API fails

        if self.miles_driven and self.duration and self.duration > 0:
            self.average_speed = self.miles_driven / self.duration
        else:
            self.average_speed = 0

        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.date}: {self.miles_driven} miles at {self.average_speed:.2f} mph"

# Tracks GPS-based start and end coordinates.
# Uses Google Maps API to get distance and time between coordinates (we'll calculate this next).
class Trip(models.Model):
    start_lat = models.FloatField()  # Latitude of the start location
    start_lng = models.FloatField()  # Longitude of the start location
    end_lat = models.FloatField()  # Latitude of the end location
    end_lng = models.FloatField()  # Longitude of the end location
    distance = models.FloatField()  # In miles
    duration = models.FloatField()  # In seconds
    average_speed = models.FloatField()  # In mph
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip from ({self.start_lat}, {self.start_lng}) to ({self.end_lat}, {self.end_lng})"

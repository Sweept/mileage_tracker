from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MileageEntryViewSet

router = DefaultRouter()
router.register(r'mileage', MileageEntryViewSet)  # Register the API route

urlpatterns = [
    path('', include(router.urls)), # Include generated API endpoints
]
# Automatically creates RESTful URLs for CRUD actions.
# Exposes:
# GET /api/mileage/ → List all mileage entries
# POST /api/mileage/ → Create a new mileage entry
# GET /api/mileage/{id}/ → Retrieve a specific entry
# PUT /api/mileage/{id}/ → Update an entry
# DELETE /api/mileage/{id}/ → Delete an entry
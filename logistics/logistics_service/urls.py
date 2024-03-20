from django.urls import path
from . import views

'''from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register("", views.UserViewSet)'''

urlpatterns = [
    path('get_details', views.shipment_details.as_view()),
]
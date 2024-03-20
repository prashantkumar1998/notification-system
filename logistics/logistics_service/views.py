from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tracking


class shipment_details(APIView):
    def get(self,request):
        data = request.data
        tracking_id = data.get('tracking_id')
        if tracking_id:
            tracking_details = tracking.objects.filter(tracking_id = tracking_id)
        else:
            return Response(f"tracking_id is required",status=status.HTTP_400_BAD_REQUEST)

        if tracking_details:
            final_resp = {
                "name": tracking_details['name'],
                "status": tracking_details['status'],
                "email": tracking_details['email']
            }
        else:
            return Response({},status=status.HTTP_201_FETCHED)

        return Response(final_resp,status=status.HTTP_201_FETCHED)



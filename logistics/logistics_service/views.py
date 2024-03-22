from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tracking


class shipment_details(APIView):
    def get(self,request):
        tracking_id = request.query_params.get('tracking_id')
        if tracking_id:
            tracking_details = Tracking.objects.filter(tracking_id = tracking_id)
        else:
            return Response(f"tracking_id is required",status=status.HTTP_400_BAD_REQUEST)

        if tracking_details:
            final_resp = {
                "name": tracking_details[0].name,
                "status": tracking_details[0].status,
                "email": tracking_details[0].email
            }
        else:
            return Response({},status=status.HTTP_200_OK)

        return Response(final_resp,status=status.HTTP_200_OK)



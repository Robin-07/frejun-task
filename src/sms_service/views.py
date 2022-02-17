from rest_framework import views, response, status
from .serializers import InboundSMSSerializer, OutboundSMSSerializer


class InboundSMSAPIView(views.APIView):
    def post(self, request):
        serializer = InboundSMSSerializer(data=request.data, context = {"user" : request.user})
        serializer.is_valid(raise_exception=True)
        return response.Response(data=serializer.save(), status=status.HTTP_200_OK)


class OutboundSMSAPIView(views.APIView):
    def post(self, request):
        serializer = OutboundSMSSerializer(data=request.data, context = {"user" : request.user})
        serializer.is_valid(raise_exception=True)
        return response.Response(data=serializer.save(), status=status.HTTP_200_OK)
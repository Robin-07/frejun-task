from django.urls import path
from rest_framework import routers
from .views import InboundSMSAPIView, OutboundSMSAPIView

urlpatterns = [
    path("inbound/sms/", InboundSMSAPIView.as_view()),
    path("outbound/sms/", OutboundSMSAPIView.as_view())
]
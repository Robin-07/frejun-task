from asyncio.windows_events import NULL
from rest_framework import serializers
from .utils import validate_input
from .models import Account, PhoneNumber
from django.core.cache import cache


class InboundSMSSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        response = {"message" : "", "error" : ""}
        validate_input(data, response)
        if response["error"]:
            raise serializers.ValidationError(response)
        account = Account.objects.get(username=self.context.get("user").username)
        number_list = PhoneNumber.objects.filter(account=account.id).values_list('number', flat=True)
        if data.get("to") not in number_list:
            response["error"] = "to parameter not found"
            raise serializers.ValidationError(response)
        response["message"] = "inbound sms ok"
        return response

    def create(self, validated_data):
        return validated_data


class OutboundSMSSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        response = {"message" : "", "error" : ""}
        validate_input(data, response)
        if response["error"]:
            raise serializers.ValidationError(response)
        response["message"] = "outbound sms ok"
        return response
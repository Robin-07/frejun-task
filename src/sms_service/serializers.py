from rest_framework import serializers
from .utils import validate_input


class InboundSMSSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        response = {"message" : "", "error" : ""}
        validate_input(data, response)
        if response["error"]:
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
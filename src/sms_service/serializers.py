from django.core.cache import cache
from rest_framework import serializers

from .models import Account, PhoneNumber
from .utils import validate_input


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
        return data

    def create(self, validated_data):
        text = validated_data.get("text")
        if text in ["STOP", "STOP\n", "STOP\r", "STOP\r\n"]:
            _from = validated_data.get("from")
            _to = validated_data.get("to")
            if not cache.get(_from):
                cache.set(_from, _to, timeout=14400)
        response = {"message" : "inbound sms ok", "error" : ""}
        return response


class OutboundSMSSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        response = {"message" : "", "error" : ""}
        validate_input(data, response)
        if response["error"]:
            raise serializers.ValidationError(response)
        account = Account.objects.get(username=self.context.get("user").username)
        number_list = PhoneNumber.objects.filter(account=account.id).values_list('number', flat=True)
        if data.get("from") not in number_list:
            response["error"] = "from parameter not found"
            raise serializers.ValidationError(response)
        return data

    def create(self, validated_data):
        response = {"message" : "", "error" : ""}
        _from = validated_data.get("from")
        _to = validated_data.get("to")
        if cache.get(_from) == _to:
            response["error"] = f"sms from {_from} to {_to} blocked by STOP request"
            return response
        cache_key = _from + " count"
        total_requests = cache.get(cache_key)
        if not total_requests:
            cache.set(cache_key, 1, timeout=86400)
        elif total_requests < 5:
            cache.set(cache_key, total_requests + 1)
        else:
            response["error"] = f"limit reached for from {_from}"
            return response
        response["message"] = "outbound sms ok"
        return response

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, force_authenticate

from .models import Account, PhoneNumber


class InboundSMSTestCase(APITestCase):
    def setUp(self):
        User.objects.create(username='azr1', password='20S0KPNOIM')
        account = Account.objects.create(username='azr1', auth_id='20S0KPNOIM')
        PhoneNumber.objects.create(number='4924195509198', account=account)

    def test_missing_field(self):
        data = {
            "from" : "4924195509198",
            "to" : "4924195509196"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/inbound/sms/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_field(self):
        data = {
            "from" : "4924195509198",
            "to" : "4924195509196",
            "text" : ""
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/inbound/sms/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_to_not_found(self):
        data = {
            "from" : "4924195509198",
            "to" : "4924195509196",
            "text" : "Hello"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/inbound/sms/", data)
        self.assertEqual(response.data, {"message" : "", "error" : "to parameter not found"})


class OutboundSMSTestCase(APITestCase):
    def setUp(self):
        User.objects.create(username='azr1', password='20S0KPNOIM')
        account = Account.objects.create(username='azr1', auth_id='20S0KPNOIM')
        PhoneNumber.objects.create(number='4924195509198', account=account)

    def test_missing_field(self):
        data = {
            "from" : "4924195509198",
            "text" : "Hello"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/outbound/sms/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_field(self):
        data = {
            "from" : "198",
            "to" : "4924195509196",
            "text" : "Hello"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/outbound/sms/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_from_not_found(self):
        data = {
            "from" : "4924195509196",
            "to" : "4924195509198",
            "text" : "Hello"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        response = self.client.post("/outbound/sms/", data)
        self.assertEqual(response.data, {"message" : "", "error" : "from parameter not found"})

    def test_rate_limit(self):
        data = {
            "from" : "4924195509198",
            "to" : "4924195509196",
            "text" : "Hello"
        }
        user = User.objects.all().first()
        self.client.force_authenticate(user=user)
        for i in range(50):
            response = self.client.post("/outbound/sms/", data, format='json')
        self.assertEqual(response.data, 
        {"message" : "", "error" : "limit reached for from 4924195509198"})

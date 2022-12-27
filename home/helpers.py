import random
import requests

from django.conf import settings

def send_otp_to_mobile(mobile,otp=None):
    try:
        if otp==None:
            otp = random.randint(100000,999999)
        url = f'https://2factor.in/API/V1/{settings.API_KEY}/SMS/{mobile}/{otp}'
        # curl --location --request GET 'https://2factor.in/API/V1/XXXX-XXXX-XXXX-XXXX-XXXX/SMS/+919999999999/12345/OTP1'
        response = requests.get(url)
        print(response)
        print(otp)
        return otp
    except Exception as e:
        print(e)
        return None

from django.conf import settings
import boto3


def send_otp(phone, otp):
    ''' Sends a one time password to the user's phone number'''

    client = boto3.client(
        'sns',
        region_name=settings.REGION
    )

    response = client.publish(
        PhoneNumber="+91" + phone,
        Message="Your OTP for registration at Evento is " +
        str(otp) + ".",
        MessageStructure='string',
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'otp'
            }
        }
    )
    return response

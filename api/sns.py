from django.conf import settings
import boto3


def send_otp(user):
    ''' Sends a one time password to the user's phone number'''

    client = boto3.client(
        'sns',
        region_name=settings.REGION
    )

    response = client.publish(
        PhoneNumber="+91" + user.phone,
        Message="Your OTP for registration at Evento is " +
        str(user.otp) + ".",
        MessageStructure='string',
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'otp'
            }
        }
    )
    return response

from django.conf import settings
import boto3


def send_otp(phone, otp, reset=False):
    ''' Sends a one time password to the user's phone number'''

    client = boto3.client(
        'sns',
        region_name=settings.REGION
    )
    message = "Your OTP for registration at Evento is " + str(otp) + "."
    if reset:
        message = "Your OTP for resetting your password at Evento is " + str(otp) + "."

    response = client.publish(
        PhoneNumber="+91" + phone,
        Message=message,
        MessageStructure='string',
        MessageAttributes={
            'string': {
                'DataType': 'String',
                'StringValue': 'otp'
            }
        }
    )
    return response

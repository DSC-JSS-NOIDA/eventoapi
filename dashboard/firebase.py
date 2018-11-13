from django.conf import settings
import datetime

import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate(settings.FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred)

def send_notification_to_user(registration_token, message):

    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title=message.title,
                body=message.body,
            ),
        ),
        token=registration_token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)

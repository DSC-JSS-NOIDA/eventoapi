from django.conf import settings
from django.contrib.auth import get_user_model
import datetime
import firebase_admin
from firebase_admin import credentials, messaging

User = get_user_model()

cred = credentials.Certificate(settings.FIREBASE_CRED_PATH)
firebase_admin.initialize_app(cred)

def send_notification_to_all(message):

    registration_tokens = list(User.objects.exclude(fcm_token__isnull=True).exclude(fcm_token__exact='').values_list('fcm_token', flat=True))
    topic = 'events'
    messaging.subscribe_to_topic(registration_tokens, topic)
    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title=message["title"],
                body=message["message"],
            ),
        ),
        topic=topic,
    )

    response = messaging.send(message)
    print(response)
    messaging.unsubscribe_from_topic(registration_tokens, topic)


def send_notification_to_user(registration_token, message):

    message = messaging.Message(
        android=messaging.AndroidConfig(
            ttl=datetime.timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(
                title=message["title"],
                body=message["message"],
            ),
        ),
        token=registration_token,
    )

    messaging.send(message)

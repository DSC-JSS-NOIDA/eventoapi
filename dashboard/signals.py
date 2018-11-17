from api.models import Event
from .firebase import send_notification_to_all
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Event)
def send_notifications(sender, instance, created, **kwargs):
    print(created, "hey")
    if created:
        print(instance, "woo")
        title = instance.name
        message = f"Organized by {instance.society.name}, starts {instance.start_day} at {instance.venue}"
        send_notification_to_all({"title": title, "message": message})

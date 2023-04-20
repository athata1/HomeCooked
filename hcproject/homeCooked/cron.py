from .models import *
from timezone import timedelta

def eventUpdates():
    matches = list(Rsvp.objects.filter(rsvp_event__in=Event.objects.filter(event_time__lte=datetime.now() + timedelta(minutes=10), event_time__gte=datetime.now(), event_updates=False)))
    for match in matches:
        match.rsvp_event.event_updates=True
        match.rsvp_event.save()
        notif = Notification(notif_type=Notification.type_enum.UPDAT, notif_user=match.rsvp_user, notif_message = match.rsvp_event.event_title + " will start in 10 minutes")
        notif.save()

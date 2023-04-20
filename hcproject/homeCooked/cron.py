import datetime
import schedule
import time
import requests
'''def eventUpdates():
    matches = list(Rsvp.objects.filter(rsvp_event__in=Event.objects.filter(event_time__lte=datetime.now() + datetime.timedelta(minutes=10), event_time__gte=datetime.now(), event_updates=False)))
    print("CRON")
    for match in matches:
        match.rsvp_event.event_updates=True
        match.rsvp_event.save()
        notif = Notification(notif_type=Notification.type_enum.UPDAT, notif_user=match.rsvp_user, notif_message = match.rsvp_event.event_title + " will start in 10 minutes")
        notif.save()'''

def eventUpdates():
    print("Started")
    x = requests.get('http://localhost:8000/event/refresh')
    print(x)

if __name__ == '__main__':
    schedule.every(10).minutes.do(eventUpdates)
    while True:
        schedule.run_pending()
        time.sleep(1)
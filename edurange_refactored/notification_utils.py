import os
import datetime as dt
from edurange_refactored.user.models import Notification

def NotifyCapture(description):
    Notification.create(detail=description)

def NotifyClear():
    notification = Notification.query.all()
    for i in notification:
        i.delete()

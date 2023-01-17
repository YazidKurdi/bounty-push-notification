import os
from pushbullet import Pushbullet

API_KEY = os.getenv("PUSH_BULLET")
pb = Pushbullet(API_KEY)

def push_notification(title,body):
    pb.push_note(title,body)
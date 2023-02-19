import firebase_admin
from firebase_admin import credentials, messaging

cred = credentials.Certificate("admin_sdk.json")
firebase_admin.initialize_app(cred)

def notify_all(message):
    messaging.send(messaging.Message(
        notification=messaging.Notification('Ахтунг!', message),
        topic='public'
    ))


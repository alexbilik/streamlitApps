# send_whatsapp.py
import os
from twilio.rest import Client

# You can also set these as environment variables for safety
account_sid = os.getenv('TWILIO_ACCOUNT_SID', '')
auth_token  = os.getenv('TWILIO_AUTH_TOKEN',  '')

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',          # your Twilio Sandbox WhatsApp number
    to='whatsapp:+972522957309',  # e.g. whatsapp:+972512345678
    body='Hello from Python! 🚀'
)

print(f"Message SID: {message.sid}")

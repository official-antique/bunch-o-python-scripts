import json, random
from pathlib import Path
from twilio.rest import Client


TWILIO_ACCOUNT_SID = '<GET THIS FROM TWILIO CONSOLE>'
TWILIO_AUTH_TOKEN = '<GET THIS FROM TWILIO CONSOLE>'


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
from_number = '<GET THIS FROM TWILIO CONSOLE>'


data = json.loads(Path('data.json').read_text())


for victim in data:
	spam_list = victim['spam']
	random.shuffle(spam_list)

	for spam in random.choices(spam_list, k=3):
		client.messages.create(body=spam, from_=from_number, to='whatsapp:{}'.format(victim['number']))
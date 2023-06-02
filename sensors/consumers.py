import json

from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.models import Session

from django.contrib.auth import get_user_model
User = get_user_model()

from sensors.models import SensorReading

class SensorConsumer(WebsocketConsumer):

	groups = ["QC"]

	def connect(self):
		headers = dict(self.scope['headers'])

		session_id = headers[b'sessionid'].decode()

		session = Session.objects.get(session_key=session_id)

		session_data = session.get_decoded()

		user_id = session_data.get('_auth_user_id')
		user = User.objects.get(id=user_id)

		self.scope['user'] = user


		self.accept()

	# Receive message from the group
	def send_message(self, text_data):
		message = json.dumps({"valve" : "true", "LED" : "false"})

		# Send message to WebSocket
		self.send(text_data=message)

	def disconnect(self, close_code):
		pass

	def receive(self, text_data):
		user = self.scope['user']
		device_id = user.sensor

		text_data_json = json.loads(text_data)
		tds = text_data_json["tds"]
		pH = text_data_json["pH"]
		cond = text_data_json["cond"]

		new_obj = SensorReading(device_id=device_id, tds=tds, pH=pH, cond=cond)
		new_obj.save()
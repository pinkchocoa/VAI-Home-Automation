import paho.mqtt.client as mqtt

MQTTBROKER = "iot.eclipse.org"
PORT = 1883

def on_connect(client, userdata, flags, rc):
	print("connected with result code " + str(rc))
	client.subscribe("home/doorbell")

def on_disconnect(client, userdata, rc):
	print("Disconnected with result code " + str(rc))

def on_message(client, userdata, msg):
	print(MQTTBROKER + ': <' + msg.topic + "> : " + str(msg.payload.decode()))

#main
client=mqtt.Client()
client.on_conect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(MQTTBROKER, PORT)

client.loop_forever()

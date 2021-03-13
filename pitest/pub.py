import paho.mqtt.client as mqtt

MQTTBROKER="iot.eclipse.org"
PORT=1883
TOPIC="home/doorbell"
MESSAGE="HelloWorld"

mqttc = mqtt.Client("python_pub")
mqttc.connect(MQTTBROKER, PORT)
mqttc.publish(TOPIC, MESSAGE)
print("published to " + MQTTBROKER + ": " + TOPIC + ":" + MESSAGE)

mqttc.loop(2)

import paho.mqtt.client as mqtt
from struct import *

broker="10.0.0.42"
port=1883


def on_connect(client, userdata, flags, rc):  # The callback for when  the client connects to the broker print("Connected with result  code {0}".format(str(rc)))  
	# Print result of connection attempt 
	client.subscribe("RCControl")  
	# Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server. 
	print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
	values = unpack(">fff", msg.payload)
	print(values)


client = mqtt.Client("mqtt_sub_test")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message

client.connect(broker, port)
client.loop_forever()  # Start networking daemon

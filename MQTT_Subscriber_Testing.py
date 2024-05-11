# -*- coding: utf-8 -*-
"""
Created on Sat May 11 12:17:01 2024

@author: DELL
"""

import paho.mqtt.client as mqtt

# MQTT server details
MQTT_BROKER = "localhost"  # Your MQTT broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# MQTT broker username and password
MQTT_USERNAME = "*************" #Put your MQTT Broker Username
MQTT_PASSWORD = "*************" # Put your MQTT Broker Password

# Define a callback for received messages
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))

# Create an MQTT client
client = mqtt.Client()

# Set username and password
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Set the callback for received messages
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Subscribe to the topic
client.subscribe(MQTT_TOPIC)

# Start a loop to listen for messages
try:
    client.loop_forever()  # This keeps the subscriber running
except KeyboardInterrupt:
    print("Subscriber stopped.")
finally:
    client.disconnect()


# -*- coding: utf-8 -*-
"""
Created on Sat May 11 12:10:19 2024

@author: DELL
"""

import paho.mqtt.client as mqtt
import time

# MQTT server details
MQTT_BROKER = "localhost"  # Your MQTT broker's address
MQTT_PORT = 1883
MQTT_TOPIC = "test/topic"

# MQTT broker username and password
MQTT_USERNAME = "**********"  # Put your MQTT Broker Username      
MQTT_PASSWORD = "***********" # Put your MQTT Broker Password

# Create an MQTT client
client = mqtt.Client()

# Set username and password
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Publish messages in a loop
counter = 1
try:
    while True:
        message = f"Message {counter}: Hello, MQTT!"
        client.publish(MQTT_TOPIC, message)
        print(f"Published: {message}")
        counter += 1
        time.sleep(2)  # Wait for 2 seconds before publishing the next message
except KeyboardInterrupt:
    print("Publisher stopped.")
finally:
    client.disconnect()


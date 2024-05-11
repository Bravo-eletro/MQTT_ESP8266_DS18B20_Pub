# -*- coding: utf-8 -*-
"""
Created on Sat May 11 12:19:27 2024

@author: DELL
"""

import paho.mqtt.client as mqtt
import csv
import datetime

# MQTT server details
MQTT_BROKER = "localhost"  # If the broker is on the same Raspberry Pi
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperature"

# MQTT broker username and password
MQTT_USERNAME = "***********"  # Put your MQTT Broker Username
MQTT_PASSWORD = "************" # Put your MQTT Broker Password

# CSV file to store incoming data
CSV_FILE_PATH = "/home/pi/temperature_data.csv"

# Callback when connecting to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(MQTT_TOPIC)

# Callback when a message is received
def on_message(client, userdata, message):
    # Decode the message payload
    temperature_data = str(message.payload.decode("utf-8"))
    
    # Get the current timestamp
    current_time = datetime.datetime.now().isoformat()

    # Append the data to the CSV file
    with open(CSV_FILE_PATH, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([current_time, temperature_data])

    print(f"Received message: {message.topic} | {temperature_data}")

# Create an MQTT client
client = mqtt.Client()

# Set username and password (if required)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

# Set callbacks for connection and message received
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect(MQTT_BROKER, MQTT_PORT, 60)

# Start a loop to listen for messages
client.loop_forever()


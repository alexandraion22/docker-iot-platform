import paho.mqtt.client as mqtt
import json

def _on_connect(client, userdata, flags, rc):
	print("Client connected")

def _create_client():

	client = mqtt.Client()
	client.on_connect = _on_connect

	#inlocuire cu adresa ip obtinuta din docker node inspect self
	client.connect("10.0.2.15")
	client.loop_start()
	return client

def close_client(client):
	client.disconnect()
	client.loop_stop()

def main():

	mqtt_client = _create_client()

	payload = {
		"BAT": 99,
		"HUMID": 40,
		"PRJ": "SPRC",
		"TMP": 25.3,
		"status": "OK",
		"timestamp": "2019-11-26T03:54:20+03:00"
	}

	# Convert the payload to JSON format
	json_payload = json.dumps(payload)

	# Publish the payload to a specific topic
	topic = "your/topic"
	mqtt_client.publish(topic, json_payload)

	close_client(mqtt_client)


if __name__ == '__main__':
	main()
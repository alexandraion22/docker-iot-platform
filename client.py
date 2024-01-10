from datetime import datetime, timezone, timedelta
import paho.mqtt.client as mqtt
import random
import json
import time

def _on_connect(client, userdata, flags, rc):
	print("Client connected")

def _create_client():

	client = mqtt.Client()
	client.on_connect = _on_connect

	client.connect("0.0.0.0")
	client.loop_start()

	return client

def close_client(client):
	client.disconnect()
	client.loop_stop()

def main():

	mqtt_client = _create_client()

	random.seed(datetime.now)

	# Loop infinit - trimite o serie de mesaje la cate un minut
	while (True):
		topics = ["UPB/RPi_"+str(random.randint(0,10)), "Sensors/Mongo", "Example/Gas"]
		# Trimitere cate 10 mesaje pe topicurile "UPB/RPi_(num)", "Alexandra/Mongo", "Example/Gas"
		for topic in topics:
			for i in range(0,50):
				payload = {
					"BAT": round(random.uniform(0,100),2),
					"HUMID": round(random.uniform(0,50),2),
					"PRJ": "SPRC",
					"TMP": round(random.uniform(0,40),2),
					"status": "OK",
					"timestamp": (datetime.now(timezone.utc) -timedelta(minutes=i*20)).strftime('%Y-%m-%dT%H:%M:%S%z')
				}
				# Convert the payload to JSON format
				json_payload = json.dumps(payload)
				# Publish the payload
				mqtt_client.publish(topic, json_payload)
				print(f"Client sent {payload} on topic {topic}")


		topic = "Dorinel/"+ random.choice(["Zeus","Poseidon","Hades","Athena","Artemis"])
		# Trimitere 10 mesaje pe topic "Dorinel/(nume_zeu)"
		for _ in range(0,10):
			payload = {
				"Alarm": random.randint(0,20),
				"AQI": random.randint(0,50),
				"RSSI": random.randint(0,100),
			}
			# Convert the payload to JSON format
			json_payload = json.dumps(payload)
			# Publish the payload
			mqtt_client.publish(topic, json_payload)
			print(f"Client sent {payload} on topic {topic}")

		time.sleep(60)


if __name__ == '__main__':
	main()
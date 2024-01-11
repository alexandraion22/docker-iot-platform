import paho.mqtt.client as mqtt
import logging as log
import re

from influxdb import InfluxDBClient
from datetime import datetime
from json import loads
from os import getenv

def __is_float(str):
	try:
		float(str)
		return True
	except ValueError:
		return False
	
def _on_message(client, influxDbClient, message):

	# Verificare daca topic-ul este corect (locatie/statie)
	if not re.match(r'^[^/]+/[^/]+$', message.topic):
		return

	log.info(f"Received a message by topic [{message.topic}]")
	
	# Obtinere denumire locatie si statie
	source_split = message.topic.split('/')
	location = source_split[0]
	station = source_split[1]

	topicWDots =  message.topic.replace('/','.')
	data = loads(message.payload)

	# Verificare existenta timestamp
	timeStamp = datetime.now()
	if 'timestamp' in data:
		timeStamp = datetime.strptime(data['timestamp'],'%Y-%m-%dT%H:%M:%S%z')
		log.info(f"Data timestamp is: {timeStamp}")
	else:
		log.info("Date timestamp is NOW")

	json_body = []

	# Filtrare lista de tupluri
	data = [elemPair for elemPair in data.items() if __is_float(elemPair[1])]		
	for key, value in data:
		log.info(f"{topicWDots}.{key} {value}")
		json_body.append({
			'measurement': f'{station}.{key}',
			'tags': {
				'location': location,
				'station': station
			},
			'time': timeStamp.strftime('%Y-%m-%dT%H:%M:%S%z'),
			'fields': {
				'value': value
			}
		})

	
	# Trimitere date in InfluxDB (daca avem ce)
	if json_body:
		influxDbClient.write_points(json_body)

def main():
	
	logType = log.INFO if getenv('DEBUG_DATA_FLOW') == 'true' else log.ERROR

	log.basicConfig(
		format='%(asctime)s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		level=logType
	)

	# Initiere client DB
	influxDbClient =  InfluxDBClient('sprc3_influxdb')
	influxDbClient.switch_database('iot')

	# Initiere client MQTT
	mqtt_cl = mqtt.Client(userdata=influxDbClient)
	mqtt_cl.on_message = _on_message
	mqtt_cl.connect('sprc3_broker')
	
	log.info('Connected to MQTT')
	
	mqtt_cl.subscribe('#')
	mqtt_cl.loop_forever()


if __name__ == "__main__":
	main()

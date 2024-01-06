from json import loads, dumps
import logging as log

import paho.mqtt.client as mqtt


def _on_message(client, userdata, message):
    print(message.topic+" "+str(message.payload))
    
def main():
	log_level = log.INFO

	log.basicConfig(
		format='%(asctime)s %(message)s',
		datefmt='%Y-%m-%d %H:%M:%S',
		level=log_level
	)

	mqtt_cl = mqtt.Client()
	mqtt_cl.on_message = _on_message

	log.info(f'Before connecting')
	mqtt_cl.connect('sprc3_broker')
	log.info(f'After connecting')
	mqtt_cl.subscribe('#')
	mqtt_cl.loop_forever()


if __name__ == "__main__":
	main()

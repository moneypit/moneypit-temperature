import sys
import Adafruit_DHT
import redis
import json
import datetime

# Load config
with open(sys.argv[1]) as f:
    config = json.load(f)

# Instantiate redis client
rClient = redis.Redis(config['redis']['host'],config['redis']['port'])

temp_sensors = config['temp']

temperatureObject = {}

for i, temp_sensor in enumerate(temp_sensors):

    temperatureObject['timestamp'] = datetime.datetime.now().isoformat()

    sensor_name = temp_sensor['name']
    sensor = temp_sensor['sensor']
    pin = temp_sensor['pin']

    temperatureObject[sensor_name] = {}

    temperatureObject[sensor_name]['humidity'], temperatureObject[sensor_name]['temperatureC'] = Adafruit_DHT.read_retry(sensor, pin)
    temperatureObject[sensor_name]['temperatureF'] = (temperatureObject['temperatureC'] * 1.8) + 32

rClient.set('temperature',json.dumps(temperatureObject))
rClient.save()

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
print temp_sensors;

temperatureObject = {}

for i, temp_sensor in enumerate(temp_sensors):

    temperatureObject['timestamp'] = datetime.datetime.now().isoformat()

    sensor_name = temp_sensor['name']
    sensor = temp_sensor['sensor']
    pin = temp_sensor['pin']

    temperatureObject[sensor_name] = {}
    
    print Adafruit_DHT.read(sensor, pin)
   
    temperatureObject[sensor_name]['humidity'], temperatureObject[sensor_name]['temperatureC'] = Adafruit_DHT.read(sensor, pin)
    
    if temperatureObject[sensor_name]['temperatureC'] is None:
    	temperatureObject[sensor_name]['humidity'] = 0.0
        temperatureObject[sensor_name]['temperatureC'] = 0.0
        temperatureObject[sensor_name]['temperatureF'] = 0.0
    else:
        temperatureObject[sensor_name]['temperatureF'] = (temperatureObject[sensor_name]['temperatureC'] * 1.8) + 32


print temperatureObject
rClient.set('temperature',json.dumps(temperatureObject))
rClient.save()

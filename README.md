# moneypit-temperature

Used to monitor temperature on supply / exhaust side of miner racks.

- [QTY 2] DHT22 Temperature sensor (https://www.adafruit.com/product/385)

## Dependencies

- Git
   `sudo apt-get install git`

- Python 2 w/ pip
  `sudo apt-get install python-pip`
  `sudo python -m pip install --upgrade pip setuptools wheel`

- Redis Server / Python Client
   `sudo apt-get install redis-server`
   `sudo pip install redis`

- Npm / Node
   `sudo apt-get install npm`
   `sudo apt-get install nodejs`

- PHP CLI / Curl
   `sudo apt-get install php7.0-cli`
   `sudo apt-get install php7.0-curl`

- Temp Sensor Python Library
  `sudo pip install Adafruit_DHT`

- A remote `elasticsearch` to post stats to

> Recommend running `sudo apt-get update` if running into issues installing dependencies

## Install

- Clone repo `git clone https://github.com/moneypit/moneypit-temperature`

- Rename `config_sample.json` to `config.json`

- Update config

```

{
  "device": "moneypit-temperature",
  "location": "moneypitmine",
  "elasticsearch": {
    "hosts": [
      "https://elastic:xxx.us-east-1.aws.found.io:9243"
    ],
    "stats_index": "mp-temp-stats"
  },
  "redis": {
    "host": "localhost",
    "port": "6379"
  },
  "temp": [
    {
      "name": "rack-supply",
      "sensor": 22,
      "pin": "4"
    },
    {
      "name": "rack-exhaust",
      "sensor": 22,
      "pin": "5"
    }
  ]
}


```

> You should update pins if sensor is plugged into different GPIO ports than shown.  Also more temp sensors can be added to config.

- Enable `redis-server` service is start on reboot

`sudo systemctl enable redis-server`

- Configure node / redis / fan rpm monitoring script to start on reboot using `/etc/rc.local`

```

	#!/bin/sh -e
	#
	# rc.local
	#
	# This script is executed at the end of each multiuser runlevel.
	# Make sure that the script will "exit 0" on success or any other
	# value on error.
	#
	# In order to enable or disable this script just change the execution
	# bits.
	#
	# By default this script does nothing.

	# Print the IP address
	_IP=$(hostname -I) || true
	if [ "$_IP" ]; then
	  printf "My IP address is %s\n" "$_IP"
	fi

	# Start moneypit-temperature node app / api
	sudo /usr/bin/npm start --cwd /home/pi/moneypit-temperature --prefix /home/pi/moneypit-temperature &

	exit 0

```

- From within the `./moneypit-fan-controller-folder` install PHP / Node dependencies

  ```
  wget https://raw.githubusercontent.com/composer/getcomposer.org/1b137f8bf6db3e79a38a5bc45324414a6b1f9df2/web/installer -O - -q | php -- --quiet
  php composer.phar install
  npm install
  ```

- Setup the following cron jobs:

```

* * * * * python /home/pi/moneypit-fan-controller/scripts/fetch_temp.py /home/pi/moneypit-temperature/config.json
* * * * * php /home/pi/moneypit-temperature/scripts/post_stats.php

```

- Reboot the device to start processes

```
sudo reboot
```

## APIs

`GET /` => Swagger docs

`GET /temperature` => Returns temperature details and last temp details was captured

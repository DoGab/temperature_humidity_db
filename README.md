# Temperature and Humiidity Sensor Graphic

## Table of contents

1. [Module description - What the module does](#module-description)
2. [Setup](#setup)
  * [Requirements](#requirements)
  * [Installation](#Installation)
3. [Usage - Configuration options and additional functionality](#usage)

## Module description

This module can be used to visualize temperature and humidity data read from the adafruit sensor AM2302.

## Setup

### Requirements
#### Hardware
* Raspberry Pi
* Temperature/Humidity Sensor (DHT11, 22 / AM2302)

#### Software
* Raspian (Jessie or Stretch)
* php5 / php7.0
* php5-sqlite / php7.0-sqlite
* libapache2-mod-php5 / libapache2-mod-php7.0
* apache2 (2.4.10)
* sqlite3 (3.8.7.1)
* Adafruit_Python_DHT (build-essential python-dev git)

### Installation
The installtion covers the software installation to read sensor data and display it on a webserver.
1. Connect the sensor to the GPIO Ports of the Raspberry Pi
2. Install the sensors Adafruit library
    * Described here: [Adafruit_Python_DHT](https://github.com/adafruit/Adafruit_Python_DHT)
3. Setup an apache webserver, install sqlite3 and php5 or php7
4. Copy the files from /var/www/html to your documentroot
    * Adjust the sqlite3 database path in the `sqlite_query.php` script
5. Copy the file from the bin folder to your prefered location
    * Adjust the files variables to specify your sqlite3 database path and name
6. Create a cronjob which points to your `sensor_to_db.py` in the following format:
    * */5 * * * * python /home/pi/git-projects/temperature_humidity_db/sensor_to_db.py 2302 4 > /dev/null 2>&1

## Usage

Open your Raspberry pis ip address to see if the webserver is running. If it does, after at least 10 minutes, you should see a beautiful graph with your sensors data.


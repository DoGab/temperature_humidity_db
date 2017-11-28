#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# Version: 0.1
# Author: Dominic Gabriel

import sys
import Adafruit_DHT
import sqlite3
import datetime

# Parse command line parameters.
sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('usage: sudo ./Adafruit_DHT.py [11|22|2302] GPIOpin#')
    print('example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO #4')
    sys.exit(1)

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
timestamp = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())

if temperature is None and humidity is None:
  sys.exit(1)
else:
  print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
  print('Timestamp: %s' % timestamp)

temperature = '{0:0.1f}'.format(temperature)
humidity = '{0:0.1f}'.format(humidity)

db_name          = 'thermvisdb'
db_path          = '/opt/thermvis/database/'
data_table_name  = 'sensordata'
alarm_table_name = 'alarmdata'

# Connect to sqlite3 db
conn = sqlite3.connect(db_path + db_name)
c = conn.cursor()

# Create table with columns
# - timestamp
# - temperature
# - humidity
sql='create table if not exists ' + data_table_name + ' (timestamp text, temperature real, humidity real)'
sql='create table if not exists ' + alarm_table_name + ' (alarmid integer primary key autoincrement, sensorid integer, sensorname text, temperature_gt real default null, temperature_lt real default null, humidity_gt real default null, humidity_lt real default null)'
c.execute(sql)

# Insert data into table
sql='insert into ' + data_table_name + " values ('" + timestamp + "'," + temperature + ',' + humidity + ')'
c.execute(sql)
#print('SQL: %s' % sql)

conn.commit()
conn.close()

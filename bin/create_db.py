#!/usr/bin/python

# Version: 0.1
# Author: Dominic Gabriel

import sys
import sqlite3
import datetime
import ConfigParser

#config_file      = '/etc/thermvis/thermvis.conf'
#db_path          = '/opt/thermvis/database/'
#db_name          = 'thermvisdb'
#data_table_name  = 'sensordata'
#alarm_table_name = 'alarmdata'


def create_connection(db_file):
  try:
    conn = sqlite3.connect(db_file)
    return conn
  except Error as e:
    print(e)

  return None

def create_table(conn, create_table_sql):
  try:
    c = conn.cursor()
    c.execute(create_table_sql)
  except Error as e:
    print(e)

def main():
  config_file       = '/etc/thermvis/thermvis.conf'
  db_path           = '/opt/thermvis/database/'
  db_name           = 'thermvisdb'
  data_table_name   = 'sensordata'
  alarm_table_name  = 'alarmdata'
  login_table_name  = 'login'
  person_table_name = 'person'
  sensor_table_name = 'sensor'
  

  config = ConfigParser.ConfigParser()
  config.read(config_file)
  smtp_server = config.get('SMTP', 'SmtpServer')

  #sql_create_data_table = """create table if not exists ?
  #(dataid integer primary key, sensorid integer not null, timestamp text not null, temperature real not null, humidity real not null)
  #""", (data_table_name)
  sql_create_data_table  = 'create table if not exists ' + data_table_name + ' (timestamp text, temperature real, humidity real)'
  #sql_create_alarm_table = """create table if not exists ?
  #(alarmid integer primary key autoincrement, sensorid integer not null, value real not null, comparator text check( comparator IN ('lt','gt') ) not null)
  #""", (alarm_table_name)
  sql_create_alarm_table = 'create table if not exists ' + alarm_table_name + ' (alarmid integer primary key autoincrement, sensorid integer, sensorname text, temperature_gt real default null, temperature_lt real default null, humidity_gt real default null, humidity_lt real default null)'
  #sql_create_login_table = """create table if not exists ?
  #(id int primary key, username text not null unique, password text not null)
  #""", (login_table_name)
  sql_create_login_table = 'create table if not exists ' + login_table_name + ' (username text primary key, password text)'
  sql_create_person_table = 'create table if not exists ' + person_table_name + ' (persid integer primary key autoincrement, firstname text, lastname text, email text)'
  sql_create_sensor_table = 'create table if not exists ' + sensor_table_name + ' (sensorid integer primary key autoincrement, description text, gpioport integer)'

  conn = create_connection(db_path + db_name)

  if conn is not None:
    create_table(conn, sql_create_data_table)
    create_table(conn, sql_create_alarm_table)

    conn.commit()
    conn.close()
  else:
    print("Error! cannot create the database connection.")

if __name__ == '__main__':
  main()

# Connect to sqlite3 db
#conn = sqlite3.connect(db_path + db_name)
#c = conn.cursor()

# Create table with columns
# - timestamp
# - temperature
# - humidity
#sql='create table if not exists ' + data_table_name + ' (timestamp text, temperature real, humidity real)'
#sql='create table if not exists ' + alarm_table_name + ' (alarmid integer primary key autoincrement, sensorid integer, sensorname text, temperature_gt real default null, temperature_lt real default null, humidity_gt real default null, humidity_lt real default null)'
#c.execute(sql)

# Insert data into table
#sql='insert into ' + data_table_name + " values ('" + timestamp + "'," + temperature + ',' + humidity + ')'
#c.execute(sql)
#print('SQL: %s' % sql)

#conn.commit()
#conn.close()

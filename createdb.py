'''  
 
Created on Feb 13, 2016  
 
@author: Mike  
 
#code to create database, tables and import data from xls file  
 
'''  
  
import MySQLdb  
 
 
# Open database connection  
 
db = MySQLdb.connect("localhost","root","")  
 
# prepare a cursor object using cursor() method  
 
cursor = db.cursor()  
 
# Below line  is hide your warning   
 
cursor.execute("SET sql_notes = 0; ")  
 
# create db   
 
sql='create database IF NOT EXISTS wifi_track'  
 
cursor.execute(sql)  
   
 
# creating tables  
 
cursor.execute("SET sql_notes = 0; ")  
cursor.execute("use wifi_track;") 
cursor.execute("create table IF NOT EXISTS macs (ID int NOT NULL AUTO_INCREMENT, mac_address_mask varchar(30), device_model varchar(20), PRIMARY KEY (ID));") 
 
cursor.execute("create table IF NOT EXISTS ssid (ID int NOT NULL AUTO_INCREMENT, name varchar(55), bssid varchar(255), channel int, device_mac int, PRIMARY KEY (ID));")  
 
cursor.execute("create table IF NOT EXISTS devices (ID int NOT NULL AUTO_INCREMENT, device_mac int, PRIMARY KEY (ID));")  
 
cursor.execute("create table IF NOT EXISTS geo (ID int NOT NULL AUTO_INCREMENT, ssid_name varchar (55), coordinates varchar(255), PRIMARY KEY (ID));")  
 
cursor.execute("create table IF NOT EXISTS devices_macs (ID int NOT NULL AUTO_INCREMENT, device_mac varchar (30), device_model varchar(20), PRIMARY KEY (ID));")  
 
cursor.execute("create or replace view v_common AS select m.ID, m.device_model, s.name, g.coordinates from devices_macs m join ssid s on s.device_mac = m.device_mac join geo g on g.ssid_name =  s.name;")  
 
#print created tables  
 
cursor.execute("show tables;")  
for (table_name,) in cursor:
    print "Table " + (table_name)

cursor.execute("SET sql_notes = 1; ")  
 

# Commit your changes in the database  
 
db.commit()  
 
# disconnect from server  
 
db.close()
 
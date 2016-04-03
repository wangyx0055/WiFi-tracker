import sys				#Always there
from PyQt4 import QtGui, QtCore 	#QtGui - imports GUI; Qtcore - imports event handling (to make buttons do things)
import wifi_mon
import json					
import os
import logging
from wifi_mon import iwconfig
from PyQt4.Qt import QWebView, QUrl
logging.getLogger("scapy.runtime").setLevel(logging.ERROR) # Shut up Scapy
from scapy.all import *
conf.verb = 0 # Scapy I thought I told you to shut up
import os
import sys
import time
from threading import Thread, Lock
from subprocess import Popen, PIPE
from os import devnull
from subprocess import call
from signal import SIGINT, signal
import argparse
import socket
import struct
import fcntl
import probe_scan
import psycopg2
import sys
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class Window(QtGui.QMainWindow):				#Application inherit from QtGui.QMainWindow (also QWidget can be used); Window is an object

	# ===== Window ===== 

	def __init__(self):					#Defines Window (init method); from now, 'self' will reference to the window; 
								#everytime a window object is made the init method runs; Core of the application is in __init__
		
		super(Window, self).__init__()				#Super returnd parent object (which is QMainWindow);  () - Empty parameter
		self.setGeometry(50, 50, 1000, 700)			#Set the geometry of the window. (starting X; starting Y; width; length)
		self.setWindowTitle("Wifi Probe Scanner Project")		#Set title of the window (Window name)
		self.setWindowIcon(QtGui.QIcon('itb.png'))		#Set the image in the window name (doesn't seem to work in Linux)

	# ===== Main Menu ===== 
									#Menu Choices
		monitorMode = QtGui.QAction("& Enable Monitor Mode", self)	#Defines action for Wi-Fi Monitor Mode
		monitorMode.setShortcut("Ctrl+M")			#Sets shortcut for Wi-Fi monitor mode action
		monitorMode.setStatusTip("Wi-Fi Monitor Mode")		#Information shown in the status bar (doesn't work in the linux)
		monitorMode.triggered.connect(self.wifi_monitor)	#Calls the method for enabling Wi-Fi monitor mode

		launchScan = QtGui.QAction("& Launch Probe Scan", self)	#Defines action for Scanning Probes
		launchScan.setShortcut("Ctrl+S")			#Sets shortcut for action
		launchScan.setStatusTip("Start Wi-Fi Scan")		#Information shown in the status bar (doesn't work in the linux)
		launchScan.triggered.connect(self.probe_scan)		#Calls the method for scanning probes

		quitAction = QtGui.QAction("& Exit Application", self)	#Defines action
		quitAction.setShortcut("Ctrl+Q")			#Sets shortcut for action
		quitAction.setStatusTip("Terminate the Application")	#Information shown in the status bar (doesn't work in the linux)
		quitAction.triggered.connect(self.close_application)	#Calls the method for closing the application
		
		cleardb = QtGui.QAction("& Clear database from records", self)	#Defines action for truncating tables
		cleardb.setShortcut("Ctrl+D")			#Sets shortcut for action
		cleardb.setStatusTip("Clear database")		#Information shown in the status bar 
		cleardb.triggered.connect(self.clear_db)		#Calls the method for truncating tables
		
		
		plotMap = QtGui.QAction("& Generate maps from probes", self)	#Defines action for Plotting maps
		plotMap.setShortcut("Ctrl+G")			#Sets shortcut for action
		plotMap.setStatusTip("Generate maps")		#Information shown in the status bar 
		plotMap.triggered.connect(self.mapplot)		#Calls the method for generating html
		
		self.statusBar()					#Calls the status bar (to show setStatusTip), nothing else is needed!
		
									#Main Menu
		mainMenu = self.menuBar()				#menuBar object is assigned to mainMenu, because we will need to modify it/add to it
		fileMenu = mainMenu.addMenu('&Menu')			#Defines one line of menu and assigne it a name
		fileMenu.addAction(monitorMode)				#Adds action to the menu line - Wi-Fi Monitor Mode
		fileMenu.addAction(launchScan)				#Adds action to the menu line - Scanning Probes
		fileMenu.addAction(quitAction)				#Adds action to the menu line - Exit Application	
		fileMenu.addAction(cleardb)
		fileMenu.addAction(plotMap)				#Adds action to the menu line - Exit Application	
		
		self.home()						#Refers to the next method


	# ===== Main Window ===== 

	def home(self):							#Defines a method 'home' 

									#Button for Wi-Fi Monitor Mode
		btn1 = QtGui.QPushButton("Enable Monitor Mode", self)	#Defines a button with parameter name (!!! WHY PASS SELF ???)
		btn1.clicked.connect(self.wifi_monitor)			#Defines an event (through .connect), event is Monitor Mode

		btn1.resize(180, 40)					#Defines the size of the button (width; length) or PyQt suggest minimum size btn1.minimumSizeHint()
		btn1.move(50, 50)					#Defines location of the button on the screen (starting X; starting Y)
									
		
									#Button for Scanning Probes
		self.progress = QtGui.QProgressBar(self)
		self.progress.setGeometry(50, 350, 600, 20)
		
		btn2 = QtGui.QPushButton("Launch Probe Scan", self)	#Defines a button with parameter name
		btn2.clicked.connect(self.probe_scan)			#Defines an event (through .connect), event is Scanning Probes

		btn2.resize(180, 40)					#Defines the size of the button (width; length)
		btn2.move(50, 120)					#Defines location of the button on the screen (starting X; starting Y)


									#Button for Exit Application
		btn3 = QtGui.QPushButton("Exit Application", self)	#Defines a button with parameter name
		btn3.clicked.connect(self.close_application)		#Defines an event (through .connect), event is Close Application

		btn3.resize(180, 40)					#Defines the size of the button (width; length)
		btn3.move(50, 260)					#Defines location of the button on the screen (starting X; starting Y)

									#Button to generate maps from probes
		btn4 = QtGui.QPushButton("Generate maps", self)	#Defines a button with parameter name (!!! WHY PASS SELF ???)
		btn4.clicked.connect(self.mapplot)			#Defines an event (through .connect), event is Monitor Mode

		btn4.resize(180, 40)					#Defines the size of the button (width; length) or PyQt suggest minimum size btn1.minimumSizeHint()
		btn4.move(50, 190)					#Defines location of the button on the screen (starting X; starting Y)

											#Button for Exit Application
		btn5 = QtGui.QPushButton("Clear Database", self)	#Defines a button with parameter name
		btn5.clicked.connect(self.clear_db)		#Defines an event (through .connect), event is Close Application

		btn5.resize(180, 40)					#Defines the size of the button (width; length)
		btn5.move(260, 50)					#Defines location of the button on the screen (starting X; starting Y)

				
		self.show()						#Shows the application in the end (call the graphics from memory and display it)


	# ===== Methods ===== 
	
	def wifi_monitor(self):						#Method for closing application
		try:
			startmon = wifi_mon.start_mon_mode(iface)
			QtGui.QMessageBox.information(self, "Enabling Monitor Mode", "Monitor mode started on strongest interface %s"% (iface))
		except Exception, msg:
			QtGui.QMessageBox.information(self, "Enabling Monitor Mode", "Enabling monitor mode failed due to error: %s" % (msg,))
	
					
	def probe_scan(self):						#Method for closing application
		choice = QtGui.QMessageBox.question(self, "Start sniffing", "Start collecting probes on interface %s?"% (iface), QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:			#if/else statement - if yes
			print("Starting probes collection")	#Sends a message before quiting (in cmd & loggs)
			self.completed = 0
			while self.completed < 100:
				self.completed += 0.0001
				self.progress.setValue(self.completed)
			handler = probe_scan.Handler()                
			sniff = probe_scan.sniff(iface=iface,prn=handler,store=0,timeout=300)
		else:							#if/else statement - else (No)
			pass						#pass - nothing happens
	
	def mapplot(self):
		web_page = QWebView(self)
		web_page.setGeometry(450,50,500,500)
		web_page.load(QUrl("file:///var/www/html/mymap7.html"))
		web_page.show()									
		
	def close_application(self):					#Method for closing application
										#Pop up question box with yes/no option; parameters: self, Wwindow title, Question, Yes or No
		choice = QtGui.QMessageBox.question(self, "Exit Application", "Would you like to exit the application and Disable Monitor Mode?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
		if choice == QtGui.QMessageBox.Yes:			#if/else statement - if yes
			print("Disabling monitor mode.")	#Sends a message before quiting (in cmd & loggs)
			ifacemon = str(iface + 'mon')
			wifi_mon.remove_mon_iface(iface)
			os.system('service network-manager restart')
			QtGui.QMessageBox.information(self, "Disabling Monitor Mode", "Disabled Monitor mode on %s"% (iface,))
			sys.exit()					#Exit everything				
		else:							#if/else statement - else (No)
			pass						#pass - nothing happens

	def clear_db(self):
		con = psycopg2.connect(database='wifi', user='probecap', host = 'localhost', password='pass')
		con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
		cur = con.cursor()
		try:
			cur.execute('TRUNCATE TABLE station, ssid, probe;')
			QtGui.QMessageBox.information(self, "Clearing Database", "Tables truncated")
		except psycopg2.DatabaseError, e:
			print 'Error %s' % e    
		cur.close()
		con.close()

monitors, interfaces = wifi_mon.iwconfig()
iface = wifi_mon.get_iface(interfaces)
#with open('dbconf.json') as fin:
#       dbconf = json.load(fin)    
	
def run():							# Main Running Method (Function) - run()
	if os.geteuid():
		sys.exit('Please run as root')
	app = QtGui.QApplication(sys.argv)			# App definition (defines application); sys.argv allows to call
	GUI = Window()						# NO DESCRIPTION - This runs a window object (details of the object are above)
	sys.exit(app.exec_())					# NO DESCRIPTION

run()								#Call 'run' to run code



# ___Notes___
#
#  If the method belongsto PyQT, it has 'Q' in front of it, like btn = QtGui.QPushButton
#  If the method belongs to us, it doesn't have a 'Q', like self.home()

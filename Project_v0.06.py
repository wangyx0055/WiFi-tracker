import sys				#Always there
from PyQt4 import QtGui, QtCore 	#QtGui - imports GUI; Qtcore - imports event handling (to make buttons do things)
					

class Window(QtGui.QMainWindow):				#Application inherit from QtGui.QMainWindow (also QWidget can be used); Window is an object

	# ===== Window ===== 

	def __init__(self):					#Defines Window (init method); from now, 'self' will reference to the window; 
								#everytime a window object is made the init method runs; Core of the application is in __init__
		
		super(Window, self).__init__()				#Super returnd parent object (which is QMainWindow);  () - Empty parameter
		self.setGeometry(50, 50, 500, 300)			#Set the geometry of the window. (starting X; starting Y; width; length)
		self.setWindowTitle("Probe Scanner Project")		#Set title of the window (Window name)
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
		
		self.statusBar()					#Calls the status bar (to show setStatusTip), nothing else is needed!
		
									#Main Menu
		mainMenu = self.menuBar()				#menuBar object is assigned to mainMenu, because we will need to modify it/add to it
		fileMenu = mainMenu.addMenu('&Menu')			#Defines one line of menu and assigne it a name
		fileMenu.addAction(monitorMode)				#Adds action to the menu line - Wi-Fi Monitor Mode
		fileMenu.addAction(launchScan)				#Adds action to the menu line - Scanning Probes
		fileMenu.addAction(quitAction)				#Adds action to the menu line - Exit Application	
		
		self.home()						#Refers to the next method


	# ===== Main Window ===== 

	def home(self):							#Defines a method 'home' 

									#Button for Wi-Fi Monitor Mode
		btn1 = QtGui.QPushButton("Enable Monitor Mode", self)	#Defines a button with parameter name (!!! WHY PASS SELF ???)
		btn1.clicked.connect(self.wifi_monitor)			#Defines an event (through .connect), event is Monitor Mode

		btn1.resize(180, 40)					#Defines the size of the button (width; length) or PyQt suggest minimum size btn1.minimumSizeHint()
		btn1.move(50, 50)					#Defines location of the button on the screen (starting X; starting Y)


									#Button for Scanning Probes
		btn2 = QtGui.QPushButton("Launch Probe Scan", self)	#Defines a button with parameter name
		btn2.clicked.connect(self.probe_scan)			#Defines an event (through .connect), event is Scanning Probes

		btn2.resize(180, 40)					#Defines the size of the button (width; length)
		btn2.move(50, 120)					#Defines location of the button on the screen (starting X; starting Y)


									#Button for Exit Application
		btn3 = QtGui.QPushButton("Exit Application", self)	#Defines a button with parameter name
		btn3.clicked.connect(self.close_application)		#Defines an event (through .connect), event is Close Application

		btn3.resize(180, 40)					#Defines the size of the button (width; length)
		btn3.move(50, 190)					#Defines location of the button on the screen (starting X; starting Y)


	
		self.show()						#Shows the application in the end (call the graphics from memory and display it)


	# ===== Methods ===== 


	def wifi_monitor(self):						#Method for closing application
		pass

	def probe_scan(self):						#Method for closing application
		pass

	def close_application(self):					#Method for closing application
									#Pop up question box with yes/no option; parameters: self, Wwindow title, Question, Yes or No
		choice = QtGui.QMessageBox.question(self, "Exit Application", "Would you like to exit the application?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
			
		if choice == QtGui.QMessageBox.Yes:			#if/else statement - if yes
			print("Application was terminated by user.")	#Sends a message before quiting (in cmd & loggs)
			sys.exit()					#Exit everything				
		else:							#if/else statement - else (No)
			pass						#pass - nothing happens

	

def run():							# Main Running Method (Function) - run()
	app = QtGui.QApplication(sys.argv)			# App definition (defines application); sys.argv allows to call
								# this application from command line and pass arguments through commandline.
	GUI = Window()						# NO DESCRIPTION - This runs a window object (details of the object are above)
	sys.exit(app.exec_())					# NO DESCRIPTION

run()								#Call 'run' to run code



# ___Notes___
#
#  If the method belongsto PyQT, it has 'Q' in front of it, like btn = QtGui.QPushButton
#  If the method belongs to us, it doesn't have a 'Q', like self.home()

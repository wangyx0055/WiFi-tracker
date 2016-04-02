import logging
from wifi_mon import remove_mon_iface, get_mon_iface, get_iface, start_mon_mode,\
    iwconfig
from dbus.proxies import Interface
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
import sys
import struct
import json
import psycopg2
import datetime
from io import open
import telegram
import manuf
import os 
import sys
import re
from subprocess import Popen, PIPE
import argparse
from threading import Thread, Lock
import socket
import fcntl
from signal import SIGINT, signal

# declaring console colors
W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
C  = '\033[36m' # cyan
GR = '\033[37m' # gray
T  = '\033[93m' # tan



MGMT_TYPE = 0x0
PROBE_SUBTYPE = 0x04

FMT_HEADER_80211 = "<HH6s6s6sH"
WLAN_MGMT_ELEMENT = "<BB"

TO_DS_BIT = 2**9
FROM_DS_BIT = 2**10

updateoui = manuf.MacParser()
updateoui.refresh()

def parse_args():
    #Declaring arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--interface", help="Choose monitor mode interface. By default script will find the most powerful interface and starts monitor mode on it. Example: -i mon5")
    parser.add_argument("-c", "--channel", help="Listen clients on the specified channel. Example: -c 6")
    parser.add_argument("-m", "--maximum", help="Choose the maximum number of SSIDs. List of SSIDs will be emptied and re-populated after hitting the limit. Example: -m 5")
    
    return parser.parse_args()

def encodeMac(s):
    return ''.join(( '%.2x' % ord(i) for i in s ))

########################################
# Begin interface info and manipulation
########################################

def get_mon_iface(args):
    global monitor_on
    monitors, interfaces = iwconfig()
    if args.interface:
        monitor_on = True
        return args.interface
    if len(monitors) > 0:
        monitor_on = True
        return monitors[0]
    else:
            # Start monitor mode on a wireless interface
        print '['+G+'*'+W+'] Finding the most powerful interface...'
        interface = get_iface(interfaces)
        monmode = start_mon_mode(interface)
        print 'test ' + monmode
        return monmode
    
def iwconfig():
    monitors = []
    interfaces = {}
    try:
        proc = Popen(['iwconfig'], stdout=PIPE, stderr=DN)
    except OSError:
        sys.exit('['+R+'-'+W+'] Could not execute "iwconfig"')
    for line in proc.communicate()[0].split('\n'):
        if len(line) == 0: continue # Isn't an empty string
        if line[0] != ' ': # Doesn't start with space
            wired_search = re.search('eth[0-9]|em[0-9]|p[1-9]p[1-9]', line)
            if not wired_search: # Isn't wired
                iface = line[:line.find(' ')] # is the interface
                if 'Mode:Monitor' in line:
                    monitors.append(iface)
                elif 'IEEE 802.11' in line:
                    if "ESSID:\"" in line:
                        interfaces[iface] = 1
                    else:
                        interfaces[iface] = 0
    return monitors, interfaces
    
    def get_iface(Interfaces):
        scanned_aps = []
        if len(interfaces) < 1:
            sys.exit('['+R+'-'+W+'] No wireless interfaces found, bring one up and try again')
        if len(interfaces) == 1:
            for interface in interfaces:
                return interface
        
    # Find strongest interface with most wifi networks found
        for iface in interfaces:
            count = 0
            proc = Popen(['iwlist', iface, 'scan'], stdout=PIPE, stderr=DN)
            for line in proc.communicate()[0].split('\n'):
                if ' - Address:' in line: # first line in iwlist scan for a new AP
                    count += 1
            scanned_aps.append((count, iface))
            print '['+G+'+'+W+'] Networks discovered by '+G+iface+W+': '+T+str(count)+W
        try:
            interface = max(scanned_aps)[1]
            return interface
        except Exception as e:
            for iface in interfaces:
                interface = iface
                print '['+R+'-'+W+'] Minor error:',e
                print '    Starting monitor mode on '+G+interface+W
                return interface    
        
    #starting monitor mode on selected wifi_mon interface
def start_mon_mode(interface):
    print '['+G+'+'+W+'] Starting monitor mode off '+G+interface+W
    try:
        os.system('ifconfig %s down' % interface)
        os.system('iwconfig %s mode monitor' % interface)
        os.system('ifconfig %s up' % interface)
        return interface
    except Exception:
        sys.exit('['+R+'-'+W+'] Could not start monitor mode')
    #disabling monitor mode on wlan interface  
def remove_mon_iface(mon_iface):
    os.system('ifconfig %s down' % mon_iface)
    os.system('iwconfig %s mode managed' % mon_iface)
    os.system('ifconfig %s up' % mon_iface)


def stop(signal, frame):
    if monitor_on:
        sys.exit('\n['+R+'!'+W+'] Closing')
    else:
        remove_mon_iface(mon_iface)
        os.system('service network-manager restart')
        sys.exit('\n['+R+'!'+W+'] Closing')

########################################
# End of interface info and manipulation
########################################
class Handler(object):
    def __init__(self,conf):
        self.conf = confs
        self.conn = None
        
    def getDatabaseConnection(self):
    
        if self.conn == None:
            self.conn = psycopg2.connect(**confs)
            
        return self.conn

            
    def __call__(self,pkt):
        #If the packet is not a management packet ignore it
        if not pkt.type == MGMT_TYPE:
            return    
        
        #Extract the payload from the packet
        payload = buffer(str(pkt.payload))
        #Carve out just the header
        headerSize = struct.calcsize(FMT_HEADER_80211)
        header = payload[:headerSize]
        #unpack the header
        frameControl,dur,addr1,addr2,addr3,seq = struct.unpack(FMT_HEADER_80211,header)
        
        fromDs = (FROM_DS_BIT & frameControl) != 0
        toDs = (TO_DS_BIT & frameControl) != 0
        
        if fromDs and not toDs:
            srcAddr = addr3
        elif not  fromDs and not toDs:
            srcAddr = addr2
        elif not fromDs and toDs:
            srcAddr = addr2
        elif fromDs and toDs:
            return
        
        #Query the database to see the last time this station was seen
        conn = self.getDatabaseConnection()
        cur = conn.cursor()
        
        cur.execute('Select id,lastseen from station where mac = %s;',(encodeMac(srcAddr),))
        r = cur.fetchone()
        mac = encodeMac(srcAddr)
        #If mac never seen
        if r == None:
            #If seen, update the last seen time of the station 
            getmac = manuf.MacParser()
            model = getmac.get_manuf(mac)
            print model,mac
            #sending alert when new Mac is found
            bot = telegram.Bot(token='203410933:AAG6avZhedGbVsGZjgEa1x5u-DuNZ3BcjTE')
            updates = bot.getUpdates()
            chat_id = '199913115'
            bot.sendMessage(chat_id=chat_id, text='ALERT! Wifi perimeter violation Mac %s Model %s' % (mac,model,))
            #insert new mac into DB
            cur.execute("""Insert into station(mac, model, firstSeen,lastSeen) VALUES(%s, %s, current_timestamp at time zone 'utc',current_timestamp at time zone 'utc') returning id;""",(encodeMac(srcAddr),model,))
            r = cur.fetchone()
            suid = r
        else:
            suid,lastSeen = r
            cur.execute('Update station set lastSeen = %s where id = %s',(datetime.datetime.now(),suid,))
        cur.close()
        conn.commit()
        
        #If the packet subtype is not probe or beacon ignore the rest of it
        isProbe = pkt.subtype == PROBE_SUBTYPE
        if not isProbe:
            return
        
        #Extract each tag from the payload
        tags = payload[headerSize:]
        
        ssid = None
        while len(tags) != 0:
            #Carve out and extract the id and length of the  tag
            tagHeader = tags[0:struct.calcsize(WLAN_MGMT_ELEMENT)]
            tagId,tagLength = struct.unpack(WLAN_MGMT_ELEMENT,tagHeader)
            tags = tags[struct.calcsize(WLAN_MGMT_ELEMENT):]

            #The tag id must be zero for SSID
            #The tag length must be greater than zero or it is a 
            #an anonymous probe
            #The tag length must be less than or equal to 32 or it is
            #not a valid SSID

            if tagId == 0 and tagLength !=0 and tagLength <=32:
                ssid = tags[:tagLength]
                
                #Made sure what is extracted is valid ASCII
                #Psycopg2 pukes otherwise
                try:
                    ssid = ssid.decode('ascii')
                except UnicodeDecodeError:
                    ssid = None
                    continue
                
                break 
                
            tags = tags[tagLength:]
            
        if ssid != None:
            
            #Query the database to find the ssid
            cur = conn.cursor()
            cur.execute('Select id from ssid where name = %s',(ssid,))
            r = cur.fetchone()
            if r == None:
                cur.execute('Insert into ssid (name) VALUES(%s) returning id;',(ssid,))
                r = cur.fetchone()
                ssuid, = r
                print ssid
                cur.close()    
                conn.commit()
            else:
                ssuid, = r
                cur.close()
                conn.rollback()
        else:
            ssuid = None
            
            
        #Query the database for a probe by the station
        #if it was observed in the past 5 minutes,
        #don't add this one to the database                
        cur = conn.cursor()
        
        update = False
        if isProbe:
            if ssuid is not None:
                cur.execute('Select seen from probe left join ssid on probe.ssid=ssid.id where station = %s and ssid.id = %s order by seen desc limit 1;', (suid,ssuid,))
            else:
                cur.execute('Select seen from probe where station = %s and ssid is null order by seen desc limit 1;', (suid,))
            r = cur.fetchone()
            
            if r == None:
                update = True
            else:
                seen, = r 
                if (datetime.datetime.utcnow() - seen).total_seconds() > (5*60):
                    update = True
                
            if update:
                cur.execute("""Insert into probe(station,ssid,seen) VALUES(%s,%s,current_timestamp at time zone 'utc')""",(suid,ssuid,))
                cur.close()
                conn.commit()
            else:
                cur.close()
                conn.rollback()

if __name__ == "__main__":
    if os.geteuid():
        sys.exit('['+R+'-'+W+'] Please run as root')
    DN = open(os.devnull, 'w')
    lock = Lock()
    args = parse_args()
    monitor_on = None
    mon_iface = get_mon_iface(args)
    conf.iface = mon_iface
    signal(SIGINT, stop)
    iface = mon_iface   
    with open(confs) as fin:
        confs = json.load(fin) 
    handler = Handler(confs)                
        
    try:
        sniff(iface=mon_iface,prn=handler,store=0)
    except Exception, msg:
        print 'Error %s' % msg
        remove_mon_iface(iface)
        os.system('service network-manager restart')
        print '\n['+R+'!'+W+'] Closing'
        sys.exit(0)
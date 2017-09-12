__author__ = 'Ayush Agrawal, Andrew Bryan, Justin Carter, Christopher DeLaGarza, Deep Desai, Zachray Gray, Joshua Harlan, Ryan Jacobs,'\
'Ryan King, Iori Koh, Sarath Muddana, Ryan Noeske, Brett Phillips, Devin Popock, Alyssa Rios, Ammar Sheikh, Cosme Tejeda, Ryan Vanek'
__past_authors_2017__ = 'Kyle Coffey, Zitao Fang, Chris Jung, Taaha Kamal, Maximilian Patrick, Weston Reed, Tanvir Towhid, Vance Vaughn,' \
                        'Abhi Velaga, Jacob Waller, Colin Zhong'
_teacher_ = 'Taylor Hudson'
__credits__ = ['Ayush Agrawal', 'Andrew Bryan', 'Justin Carter', 'Christopher DeLaGarza', 'Deep Desai', 'Zachray Gray',
               'Joshua Harlan', 'Ryan Jacobs', 'Ryan King', 'Iori Koh', 'Sarath Muddana', 'Ryan Noeske', 'Brett Phillips', 'Devin Popock',
               'Alyssa Rios', 'Ammar Sheikh', 'Cosme Tejeda', 'Ryan Vanek', 'Kyle Coffey', 'Zitao Fang', 'Chris Jung', 'Taaha Kamal',
               'Maximilian Patrick', 'Weston Reed', 'Tanvir Towhid', 'Vance Vaughn', 'Abhi Velaga', 'Jacob Waller', 'Colin Zhong', 'Taylor Hudson']
__copyright__ = 'Copyright 2017, Allen High School Co-cirruclar Project'
__license__ = 'GPL'
__version__ = '2.0.5'
__maintainer__ = 'Christopher DeLaGarza, Deep Desai, Taylor Hudson'
__email__ = 'Taylor.Hudson@allenisd.org'
__status__ = 'Project Used'

##Sense Hat code by Computer Science 3 Class of 2017
##Special Appearance by Tanvir Towhid
##Special Thanks to The Evil Dragon King Mr. Hudson

import socket
import sys
from time import gmtime, strftime, sleep
from threading import Thread
import picamera
import csv
import os
from sense_hat import SenseHat
## Define sense from SenseHat() to use to collect data
sense = SenseHat()
sense.set_imu_config(False, True, False)
## Define variables
directory = '/'
videoLength = 60
camera = None
filename = strftime('%Y-%m-%d--%H:%M:%S') + '.csv'
## Fields of Data
fieldnames = ['time', 'temperature', 'humidity', 'pressure', 'pitch', 'roll', 'yaw', 'mag_x', 'mag_y', 'mag_z', 'acc_x', 'acc_y', 'acc_z', 'gyro_x', 'gyro_y', 'gyro_z']
logfile = None
logwriter = None

#control booleans
printReport = False
SenseHatAttached = False
CameraAttached = False
USBDrive = True

## Set up File to store collected data
if(printReport):
	logfile = open(filename, 'a')
	## Create logwriter based on fields
	logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)
	logwriter.writeheader()
	logfile.close()
## Deep and Chris socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('192.168.1.1', 10000)
print (sys.stderr, 'starting up %s port%s' % server_address)
sock.connect(server_address)
## FullScreen Changes the SenseHat Color based on RGB Value to all one Color
def FullScreen(R,G,B): #This means red, green, and blue
    Color = [R, G, B]
    screen = [
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
        Color, Color, Color, Color, Color, Color, Color, Color,
    ]
    sense.clear()
    sense.set_pixels(screen)
    return
## Set Up the SenseHat to print out data
if(SenseHatAttached):
	FullScreen(255, 0, 0)
if(CameraAttached):
	camera = picamera.PiCamera()
if(SenseHatAttached):
	FullScreen(0, 255, 0)
	sleep(15)
	sense.clear()

class myThread(Thread):
    def __init__(self, counter):
        Thread.__init__(self)
        self.counter = counter
        if counter == 6:
            self.name = 'VID'
        elif counter < 6:
            if counter % 2 == 0:
                self.name = 'REPORT'
            elif counter == 1:
                self.name = 'CAMERA' #This is for the camera.
        else:
            self.name = 'REPORT'
        self.start()

    def run(self): #Start the camera if attached
        if self.name == 'CAMERA':
            REPORT()
            if(CameraAttached):
                CAM()
        elif self.name == 'VID':
            REPORT()
            if(CameraAttached):
                VIDEO()
        else:
            REPORT()


def REPORT():
        if(printReport): ##Transfer data to a csv file
                logfile = open(filename, 'a')
                logwriter = csv.DictWriter(logfile, fieldnames=fieldnames)

        #collects data from SenseHat
        temp = sense.get_temperature()
        humidity = sense.get_humidity()
        pressure = sense.get_pressure()
        orientation = sense.get_orientation_degrees()
        mag = sense.get_compass_raw()
        acc = sense.get_accelerometer_raw()
        gyro = sense.get_gyroscope_raw()

        #send data to server
        finalData = strftime('%Y-%m-%d %H:%M:%S') + ',' + str(temp) + ',' + str(humidity) + ',' + str(pressure) + ',' + '{pitch}'.format(**orientation) + ',' + '{roll}'.format(**orientation) + ',' + '{yaw}'.format(**orientation) + ',' + '{x}'.format(**mag) + ',' + '{y}'.format(**mag) + ',' + '{z}'.format(**mag) + ',' + '{x}'.format(**acc) + ',' + '{y}'.format(**acc) + ',' + '{z}'.format(**acc) + ',' + '{x}'.format(**gyro) + ',' + '{y}'.format(**gyro) + ',' + '{z}'.format(**gyro) + ','
        finalData = str(finalData)
        print(finalData)
        print(sock.sendall(bytes(finalData, 'utf-8')))

        #print report on file
        #var printReport is a boolean turned off during testing. Only turned on during real run
        if(printReport):	
                logwriter.writerow({
                'time': strftime('%Y-%m-%d %H:%M:%S'),
                'temperature': str(temp), #This means temperature in Spanish.
                'humidity': str(humidity),
                'pressure': str(pressure),
                'pitch': '{pitch}'.format(**orientation),
                'roll': '{roll}'.format(**orientation),
                'yaw': '{yaw}'.format(**orientation),
                'mag_x': '{x}'.format(**mag), 'mag_y': '{y}'.format(**mag), 'mag_z': '{z}'.format(**mag),
                'acc_x': '{x}'.format(**acc), 'acc_y': '{y}'.format(**acc), 'acc_z': '{z}'.format(**acc),
                'gyro_x': '{x}'.format(**gyro), 'gyro_y': '{y}'.format(**gyro), 'gyro_z': '{z}'.format(**gyro)})
                logfile.close()
	
def camDir():
    return directory
def vidDir():
    return directory
def CAM():
    camera.capture(camDir() + TimeStamp()+'.jpeg')
def TimeStamp():
    return strftime('%Y-%m-%d %H:%M:%S', gmtime())
def VIDEO():
    camera.start_recording(vidDir() + TimeStamp() + '.h264')
    sleep(videoLength)
    camera.stop_recording()
def Vid(extradata):
    extradata += 1
    if(extradata == 10):
        extradata = 0
        camera.start_recoring(vidDir() + TimeStamp() + '.h264')
        sleep(videoLength)
        camera.stop_recording()
    return extradata
## Mount a USBDrive to the Pi and send data to that USB instead of saving on the Pi and using it's memory
def writtenOSUSB():
    partitionsFile = open('/proc/partitions')
    lines = partitionsFile.readlines()[2:]#Skips the header lines
    for line in lines:
        words = [x.strip() for x in line.split()]
        minorNumber = int(words[1])
        deviceName = words[3]
        if minorNumber % 16 == 0:
            path = '/sys/class/block/' + deviceName
            if os.path.realpath(path):
                if os.path.realpath(path).find('/usb') > 0:
                    print('/dev/%s' % deviceName)
                    return '/dev/%s' % deviceName

if(CameraAttached):
	camera.resolution = (1024,768)
	camera.framerate = 30
if(USBDrive):
	directory = str(writtenOSUSB()) + '/'

handshake = False
a = 0

try:
        while True:
                #handshake insures that all pis are connected to the server.
                #client sends a message to the server and waits for handshake
                #Once the handshake is achieved the client will send the sensehat data to server
                while not handshake:
                    
                    message = bytes('hi', 'utf-8')
                    print (sys.stderr, 'sending %s' % message)
                    sock.sendall(message)
                    
                    amount_received = 0
                    amount_expected = len('in')
                    
                    data = sock.recv(2048)
                    data = str(data)
                    data = data[2:len(data) - 1]
                    amount_received += len(data)
                    print(data)
                    if data == 'in':
                        handshake = True
                        print ('go message received')
                        
                count = 0
                while count < 12:
                    thread1 = myThread(count)
                    count += 1
                    sleep(5)

#finally
finally: #for the final part
        print ('closing socket') #the final thing printed
        sock.close() #finally done

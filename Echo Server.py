__author__ = 'Ayush Agrawal, Andrew Bryan, Justin Carter, Christopher DeLaGarza, Deep Desai, Zachray Gray, Joshua Harlan, Ryan Jacobs, ' \
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
##Special Thanks to Mr. Hudson
import socket
import threading
import sys
from sense_hat import SenseHat
import queue
import time
import sqlite3
import os

sense = SenseHat()
clientAmmount = 2
dataBaseName = 'database.db'
for i in range(1, clientAmmount + 1):
    print(i)

queueHandler = []
 
for i in range(clientAmmount):
    queueHandler.append(queue.Queue(maxsize = 10))

addresses = []
for i in range(clientAmmount):
    if i != 4:
        addresses.append('192.168.1.' + str(i + 2))
        print(addresses[i])

queueHandshake = queue.Queue(maxsize = clientAmmount) #change maxsize according to the number of pi's on network 

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
    time.sleep(1)
    sense.load_image('Tanvir.png')
    return

def createDB():
    db = sqlite3.connect(dataBaseName)
    db.execute('create table ServerNormalization (time_stamp text, temperature double, humidity double, pressure double, pitch double, roll double, yaw double, magnitude_x double, magnitude_y double, magnitude_z double, acceleration_x double, acceleration_y double, acceleration_z double, gyroscope_x double, gyroscope_y double, gyroscope_z double)')
    db.execute('create table BalloonTicket (time_stamp text, balloon_id int, temperature double, humidity double, pressure double, pitch double, roll double, yaw double, magnitude_x double, magnitude_y double, magnitude_z double, acceleration_x double, acceleration_y double, acceleration_z double, gyroscope_x double, gyroscope_y double, gyroscope_z double)')
    db.commit()
    return db

def openDB():
    return sqlite3.connect(dataBaseName)

def dbopen():
    if os.path.isfile(dataBaseName):
        return openDB()
    else:
        return createDB()

def parse_message(str):
    index = 0
    count = []
    while index >= 0:
        index = str.find(',')
        if index >= 0:
            TIME = str[0:(index)]
            ##print(TIME)
            str = str[index+1:]
            count.append(TIME)
    return count

def updateDataBase(db, str, balloonID):
    ##msg = parse_message(str)
    ##time = msg[0]
    ##temp = msg[1]
    ##humidty = msg[2]
    ##pressure = msg[3]
    ##pitch = msg[4]
    ##roll = msg[5]
    ##yaw = msg[6]
    ##mag_x = msg[7]
    ##mag_y = msg[8]
    ##mag_z = msg[9]
    ##acc_x = msg[10]
    ##acc_y = msg[11]
    ##acc_z = msg[12]
    ##gyro_x = msg[13]
    ##gyro_y = msg[14]
    ##gyro_z = msg[15]
    db.execute('insert into BalloonTicket (time_stamp, balloon_id, temperature, humidity, pressure, pitch, roll, yaw, magnitude_x, magnitude_y, magnitude_z, acceleration_x, acceleration_y, acceleration_z, gyroscope_x, gyroscope_y, gyroscope_z)  '
               'VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(msg[0], balloonID, msg[1],msg[2],msg[3],msg[4],msg[5],msg[6],msg[7],msg[8],msg[9],msg[10],msg[11],msg[12],msg[13],msg[14],msg[15]))
    print(msg)
    return

class ThreadedServer(object):
    def __init__(self, host, port): #Initialize all variables in ThreadedServer
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.size = 1024

    def listen(self): #listens for clients
        self.sock.listen(5)
        check = True

        q = []
        clients = []
        for i in range(1, clientAmmount + 1):
            q.append(True)
            
        whileFinish = False
        while not whileFinish: #while loop only runs if all clients are not accepted
            client, address = self.sock.accept()
            addresshost, addressport = address
            print(addresshost)
            
            #identifying and saving different clients
            #to send go message
            for i in range(clientAmmount):
                if addresshost == addresses[i]:
                    clients.append(client)
                    FullScreen(0, 255, 0)
                    print(addresshost, ':' + str(i))
            
                
            client.settimeout(60)
            
            #check for handshake
            #when server recieves client communication it will hold the server
            #once all clients are signed in this if-statement sends a go message
            #to clients that will trigger the clients to send data.
            #The server the client handshake in this way.
            if not queueHandshake.full():
                for i in range(clientAmmount):
                    if addresshost == addresses[1] and q[i]:
                        queueHandshake.put(True)

                if queueHandshake.full():
                    print('handshake acheived')
                    for i in range(clientAmmount):
                        clients[i].sendall(bytes('in', 'utf-8'))
                        time.sleep(2.0)
                        
            #The server starts a thread for each client.      
            if queueHandshake.full(): #Starts recieving information after all pis are connected
                print('Thread Start')
                for i in range(clientAmmount):
                    threading.Thread(target = handler, args = (clients[i], i)).start()
                threading.Thread(target = queues, args = ()).start()
                whileFinish = True
            

#This function runs in a separate thread and reads data from the queues.
def queues(): #This is a queue. We use it to queue things.
    b = 0;
    while True: 
        if queueHandshake.full():
            sense.show_message('go', scroll_speed = .01, text_colour = [255, 180, 50])
            for i in range(clientAmmount):
                if not queueHandler[i].empty():
                    displayStr = str(queueHandler[i].get(block = True, timeout = None))
                    displayStr = displayStr[2:len(displayStr)-1]
                    print('Received from ', addresses[i], ' : ', displayStr)
                    db = dbopen()
                    updateDataBase(db, displayStr, 0)
                    db.commit()
                    db.close()

#Each client will put their data in the queue that is reserved for them
def handler (client, clientNum):
    while True:
        data = client.recv(1024)
        queueHandler[clientNum].put(data)
       

print(sys.stderr, 'Server Starting')
sense.load_image('Tanvir.png')
server1 = ThreadedServer(host = '192.168.1.1', port = 10000)
server1.listen()
sense.clear()

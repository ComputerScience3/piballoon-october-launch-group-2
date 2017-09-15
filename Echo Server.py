## Project by Chris DeLaGarza, Deep Desai, Ryan King, Justin Carter,
##Ryan Jacobs, Zach Gray, Alyssa Rios, Iori Koh, Josh Harlan, Ayush Agarwal,
##Ryan Noeske, Cosme Tejada, Devin Popcock, Serath Mudana, Ryan Vanet, Brian Teh,
##Brett Philips, Ammar Sheikh, Andrew Bryant

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

sense = SenseHat()
clientAmmount = 2
for i in range(1, clientAmmount + 1):
    print(i)

queueHandler = []

isNotVid = []
for i in range(clientAmmount):
    isNotVid.append(True)
 
for i in range(clientAmmount):
    queueHandler.append(queue.Queue(maxsize = 10))

addresses = []
for i in range(clientAmmount):
    if i != 4:
        addresses.append('192.168.1.' + str(i + 2))
        print(addresses[i])

queueHandshake = queue.Queue(maxsize = clientAmmount) #change maxsize according to the number of pi's on network 

blue = (0,0,255)
dataPoints = 0
def dataPointsRecieved():
    global dataPoints
    if dataPoints == 64:
        dataPoints = 0
        FullScreen(0,255,0)
    sense.set_pixel(int(dataPoints%8),int(dataPoints/8),blue)
    dataPoints += 1

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
    #time.sleep(1)
    #sense.load_image('Tanvir.png')
    return

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
    msg = parse_message(str)
    yoloMsg = msg[0]
    temp = msg[1]
    hum = msg[2]
    pres = msg[3]
    ptch = msg[4]
    rol = msg[5]
    yw = msg[6]
    mag_x = msg[7]
    mag_y = msg[8]
    mag_z = msg[9]
    acc_x = msg[10]
    acc_y = msg[11]
    acc_z = msg[12]
    gyro_x = msg[13]
    gyro_y = msg[14]
    gyro_z = msg[15]
    db.execute('INSERT INTO BalloonTicket (time_stamp, balloon_id, temperature, humidity, pressure, pitch, roll, yaw, magnitude_x, magnitude_y, magnitude_z, acceleration_x, acceleration_y, acceleration_z, gyroscope_x, gyroscope_y, gyroscope_z)  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(yoloMsg, balloonID, temp, hum, pres, ptch, rol, yw, mag_x, mag_y, mag_z, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z))
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
                        time.sleep(.5)

            #The server starts a thread for each client.      
            if queueHandshake.full(): #Starts recieving information after all pis are connected
                print('Thread Start')
                for i in range(clientAmmount):
                    threading.Thread(target = handler, args = (clients[i], i)).start()
                threading.Thread(target = queues, args = ()).start()
                FullScreen(0,255,0)
                whileFinish = True
            

#This function runs in a separate thread and reads data from the queues.
def queues(): #This is a queue. We use it to queue things.
    b = 0;
    while True:
        someNotVid = False
        for i in range(clientAmmount):
            if isNotVid[i]:
                someNotVid = True
        if queueHandshake.full() and someNotVid:
            flag = True
            for i in range(clientAmmount):
                if isNotVid[i]:
                    if not queueHandler[i].empty():
                        if flag:
                            flag = True
                    else:
                        flag = False
            if flag and someNotVid:
                for i in range(clientAmmount):
                    if isNotVid[i]:
                        if not queueHandler[i].empty():
                            displayStr = str(queueHandler[i].get(block = True, timeout = None))
                            displayStr = displayStr[2:len(displayStr)-1]
                            print('Received from ', addresses[i], ' : ', displayStr)
                            db = sqlite3.connect('database.db')
                            updateDataBase(db, displayStr, 0)
                            db.commit()
                            db.close()
                dataPointsRecieved()

#Each client will put their data in the queue that is reserved for them
def handler (client, clientNum):
    while True:
        data = client.recv(1024)
        if str(data)[2:len(str(data))-1] == 'vid' or len(data) <= 0:
            isNotVid[clientNum] = False
        else:
            isNotVid[clientNum] = True
            queueHandler[clientNum].put(data)
       

print(sys.stderr, 'Server Starting')
sense.load_image('Tanvir.png')
server1 = ThreadedServer(host = '192.168.1.1', port = 10000)
server1.listen()

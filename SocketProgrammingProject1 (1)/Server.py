from Tkinter import *
from Tkinter import *
import ttk
import tkFileDialog
import tkFileDialog as filedialog
import socket
import threading
import time
import binascii

#import threading
import select, sys, Queue

class Socket ():
    def __init__(self,D_ip,protocol):
        self.protocol = protocol
        self.isfilename=False
        self.file_on = False
        self.prev = ''
        if protocol==1:
            print(protocol)
        #self.s = socket.socket()
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Ip =D_ip
            self.Port =  10000
            print ( 'starting up on ' , self.Ip)
            self.sock.bind((self.Ip,self.Port))
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            print("connected to",self.addr)
            self.C = Chat(self)
            #you dont need the if statment
            if self.C is not None:
                t = threading.Thread(target=self.wait)
                t.start()

            # while 1:
            #     print "works?"
            #     C.after(1000,C.update())
            #     #message = input(str(">> "))
            #     #GUI instead
            #     #message = message.encode()
            #     #conn.send(message)
            #     #print("message has been sent...")
            #     print("")
            #     incoming_message = self.conn.recv(1024)
            #     incoming_message = incoming_message.decode()
            #     print(" Client : ", incoming_message)
            #     print("")
        elif protocol==2:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.Ip = D_ip
            self.Port = 10000
            self.sock.bind((self.Ip,self.Port))
            print ("waiting on port",self.Port)
            self.C = Chat(self)
            t = threading.Thread(target=self.wait)
            t.start()
            #t = threading.Thread(target=self.wait)
            #t.start()
            #self.wait()
    def on_transm(self, filename):
            f = open(filename, 'rb')
            chunck_size = 1000
            to_send = []
            while True:
                data = f.read(chunck_size)
                print(data)
                to_send.append(data)
                # self.conn.send(data)
                if not data:
                    self.send_file(to_send)
                    f.close()
                    break

    def send_file(self,packets):
        self.sequence_number = 0
        self.index = 0

        #f = open(filename, 'rb')
        #chunck_size =1000
        #to_send=[]
        if self.protocol ==1:
            for i in packets:
                mesg = i + " " + str(self.sequence_number)  # assemble message as a string
                self.send_pack(mesg)
                self.start = time.time()
                self.sock.settimeout(2)
                while True:
                    self.data= self.conn.recv(1024)
                    if self.data=='Ack':
                        self.Ack= self.data
                        print self.Ack
                        break
                    elif self.data== 'NAck':
                        self.NAck=self.data
                        print self.NAck
                        self.send_file([i])
                print self.sequence_number
                print ('???????????????*')
                print (mesg)
                self.start = time.time()
                self.sequence_number+=1
                if self.sequence_number== 9:
                    self.sequence_number=0
                #t = threading.Thread(target=self.wait_before_sending())
                #t.start()
            print ('done')
            self.conn.send('/-end-/')

        elif self.protocol ==2:
            for i in packets:
                mesg = i + " " + str(self.sequence_number)  # assemble message as a string
                self.send_pack(self, mesg)
                self.sequence_number+=1
                self.start = time.time()
                #t = threading.Thread(target=self.wait_before_sending())
                print ('done')
            self.sock.send('/-end-/')

            #self.ssl_socket.sendall("EOFX")
    #def Send_file(self, file):
     #   DownloadFile = open('v1.txt', "wb")
      #  sData = ""
       # print('gon start')
        #while True:
         #   while sData:
          #      DownloadFile.write(sData)
           #     sData = self.sock.recv(1024)
            #    print type(self.data)
             #   print('got it')

              #  print sData
            #print "Download Completed"


    def wait_before_sending(self):
        self.start = time.time()
        while True:
            if time.time() - self.start < 1:
                try:
                    if self.protocol == 1:
                        received_message = self.sock.recv(1024)
                    elif self.protocol == 2:
                        self.data, self.addr = self.sock.recvfrom(1024)
                except socket.timeout:
                    print "Continue waiting..."
                    continue
                else:
                    # Corrupted ACK is handled first to avoid value errors
                    if received_message == "Bad ACK":
                        print "Sender received a corrupted ACK; keep waiting..."
                        continue
                    # If ACK is not corrupted, check if it has the correct sequence number
                    ack = int(received_message)
                    # If it does, move on to the next data set, and adjust the sequence number
                    if (ack == self.sequence_number):
                        print "ACK for ", self.sequence_number, ", send next packet"
                        sequence_number = self.NACK(self.sequence_number)
                        break
                    elif (ack == self.NACK(self.sequence_number)):
                        print "ACK received but wrong sequence number; waiti..."
                        continue
            else:
                print "Timeout. Sending packet again:"
                break

    def send_pack(self,pack):
        if self.protocol == 1:
            self.conn.send(pack)
        elif self.protocol ==2:
            self.conn.send(pack)

    def file_name(self):
        return self.isfilename
    def is_file(self):
        return
    def set_file_name(self,value):
        return self.isfilename
    def set_is_file(self,value):
        return value

    def wait(self):
        while (True):
            if self.protocol ==1:
                #print self.data
                self.data = self.conn.recv(1024)
                print type(self.data)
                if self.file_on == True:
                    print('TRue')
                    print ('here?')
                    if '/-end-/' in self.data:
                        print('closed')
                        self.saveAs.close()
                        self.file_on = False
                        self.sock.close()
                    else:
                        text2save = self.data
                        if (text2save != self.prev):
                            print "message correctly received " + text2save
                            self.conn.send('Ack')
                            text2save, received_sequence_number = self.parse_message(self.data)
                            self.prev = self.data
                            self.expected_sequence_number = received_sequence_number

                            print text2save , received_sequence_number
                        else:
                            print " duplicated message: " + text2save

                        if (received_sequence_number == self.expected_sequence_number):
                            print(text2save)
                            print
                            self.saveAs.write(text2save)
                            print ('right')
                            #self.conn.send('Ack')
                            self.expected_sequence_number = received_sequence_number + 1
                        elif received_sequence_number != self.expected_sequence_number:
                            print ('Error .. not in order')
                            #self.conn.send("Bad ACK")
                            continue
                        #else:
                        #    self.conn.send(str(self.NACK(received_sequence_number)))
                        #    print "incorrectly responds with ACK " \
                                  #+ str(self.NACK(received_sequence_number))
                         #   continue

                else:
                    if 'C:/' in self.data:
                        name = self.data.split('/')[-1]
                        self.C.label = Label(self.C.frame, text=name)
                        self.C.label.grid(column=0, row=1)
                        self.C.Cancel = Button(self.C.frame, text="Download", command=lambda: self.flag_to_Send())
                        self.C.Cancel.grid(column=1, row=1)
                        print ('other')
                        print self.data
                    elif '/send-file/' in self.data:
                        print'sending file'
                        self.on_transm(self.C.filename)
                    #self.sendTheFile()
                    else:
                        self.C.T.insert(END, (self.Ip, ": ", self.data.decode("UTF-8")))
            elif self.protocol ==2:
                self.data,self.addr = self.sock.recvfrom(124)
                if self.file_on == True:
                    print('TRue')
                    print ('here?')
                    if '/-end-/' in self.data:
                        print('closed')
                        self.saveAs.close()
                        self.file_on = False
                    else:
                        text2save = self.data
                        print('----------------')
                        print(text2save)
                        print ('----------------')
                        self.saveAs.write(text2save)
                        print (text2save)
                        print('saw that')
                else:
                    if 'C:/' in self.data:
                        name = self.data.split('/')[-1]
                        self.C.label = Label(self.C.frame, text=name)
                        self.C.label.grid(column=0, row=1)
                        self.C.Cancel = Button(self.C.frame, text="Download", command=lambda: self.flag_to_Send())
                        self.C.Cancel.grid(column=1, row=1)
                        print ('other')
                        print self.data
                    elif '/send-file/' in self.data:
                        print'sending file'
                        self.send_file(self.C.filename)

                    else:
                        self.C.T.insert(END, (self.Ip, ": ", self.data.decode("UTF-8")))
                        print self.addr







            # while 1 :
            #     data, addr = self.sock.recvfrom(1024)
            #     C.T.insert(END, (addr, ': ', data))
            #     #UDPServerSocket.sendto(bytesToSend, address)
            # while True:
            # # Wait for a connection
            #     print >> sys.stderr, 'waiting for a connection'
            #     self.conn, self.address = self.sock.accept()
            # print(self.address, " Has connected to the server and is now online ...")
            # C = Chat(self)
            # try:
            #     print >> sys.stderr, 'connection from', client_address
            #
            #     # Receive the data in small chunks and retransmit it
            #     while True:
            #         data = connection.recv(1024)
            #         print( sys.stderr, 'received "%s"' % data)
            #         if data:
            #             print (sys.stderr, 'sending data back to the client')
            #             connection.sendall(data)
            #         else:
            #             print ( sys.stderr, 'no more data from', client_address)
            #             break
            # finally:
            # # Clean up the connection
            #     connection.close()

        #
        # elif protocol ==2:
        # print(" server will start on host : ", 'localhost')
        # port = 10000
        # print D_ip
        # self.s.bind((D_ip, port))
        # print("")
        # print(" Server done binding to host and port successfully")
        # print("")
        # print("Server is waiting for incoming connections")
        # print("")
        # self.s.listen(1)
        # self.conn, self.addr = self.s.accept()
        # print(self.addr, " Has connected to the server and is now online ...")
        # C = Chat(self)
        # print("")
        # # i = 1
        # while i==1:
        #     print "works?"
        #     #message = input(str(">> "))
        #     #GUI instead
        #     #message = message.encode()
        #     #conn.send(message)
        #     #print("message has been sent...")
        #     print("")
        #     incoming_message = self.conn.recv(1024)
        #     incoming_message = incoming_message.decode()
        #     print(" Client : ", incoming_message)
        #     print("")
        #     i=i-1
    def flag_to_Send(self):
        self.saveAs = tkFileDialog.asksaveasfile(mode='w')
        if self.protocol ==1:
            self.conn.send('/send-file/')
            self.file_on = True
            print self.file_on
        elif self.protocol==2:
            self.sock.send('/send-file/')
            self.file_on = True
            print self.file_on

    def Msg(self, msg):
        print msg


    def parse_message(self,message):
        if message == "":
            return None
        list_message = message.split()
        data = message[:-1]
        received_sequence_number = int(list_message[-1])
        print data, received_sequence_number
        return data, received_sequence_number


class Start():
    def __init__(self,):
        self.T = Tk()
        self.frame = Frame()

        print('we are here')
        self.label1= Label(self.frame,text="Project1",font ='italic')
        self.label1.grid(columnspan=3)
        self.label2= Label(self.frame, text ="Enter Destination IP")
        self.label2.grid(row=1 ,column=0,sticky=W)
        self.en = Entry(self.frame)
        self.en.grid(row=1,column=1,columnspan=3)
        self.label3 = Label(self.frame,text="Protocol",)
        self.label3.grid(row=2 ,column=0,)
        self.v = IntVar()
        rb1= Radiobutton(self.frame, text="TCP", variable=self.v, value=1,command=self.selected).grid(row=2,column=1,)
        rb2= Radiobutton(self.frame, text="UDP", variable=self.v, value=2,command=self.selected).grid(row=2,column=2,)
        self.btn = Button(self.frame,text="Start Connection=>", command=lambda: self.Start_connection())
        self.btn.grid(columnspan=3)
        self.label4= Label(self.frame,text="WATING FOR CONNECRION PARTNER",fg="red" ,font='bold' )
        self.label4.grid(columnspan=3)
        self.frame.grid()

        self.T.mainloop()

    def Start_connection(self):
        print(self.en.get())
        s = self.en.get().decode()
        # ip =ipaddress.ip_address(s.encode("utf-8").decode())
        print ('******', s.encode("utf-8"))
        s = Socket(s.encode("utf-8"),self.v.get())
        #C = Chat(s)


    def selected(self):
        print self.v.get()
        if self.v.get() == 1:
            print ("hi")
        elif self.v.get() ==2 :
            print("22222")
            #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #s.bind(('localhost', 50000))
            #s.listen(1)
            #conn, addr = s.accept()
            #while 1:
                #data = conn.recv(1024)
                #if not data:
                    #break
                #conn.sendall(data)
            #conn.close()

            # import socket
            # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # s.connect(('localhost', 50000))
            # s.sendall('Hello, world')
            # data = s.recv(1024)
            # s.close()
            # print 'Received', repr(data)

        #elif self.v.get() == 2:
                #"do something"
        #else:
                #"do something"

class Chat(Socket):
    print "here"
    def __init__(self,obj):
        self.obj= obj
        self.frame = Frame()
        #self.T.title("PyChatHost")
        self.T = Text(height=20, width=100)
        self.T.grid(column=0,row=0,sticky =W)
        self.T2 = Text(self.frame,height =7, width=50)
        self.T2.grid(column =0,row =2 , sticky = EW)
        self.btn = Button(self.frame,text="Send", command=lambda:self.GetMsg())
        self.btn.grid(column=1,row =2)
        self.btn2= Button(self.frame, text="Emoji",command=lambda: emoji(self,obj))
        self.btn2.grid(column=2,row=2)
        self.Browse=Button(self.frame,text="Browse", command=lambda:self.Uploud_file())
        self.Browse.grid(column=3,row =2)
        self.frame.grid()
        s = u'that\u2019s \U0001f63b'
        print s

    def sending_file(self):

        #s = bytes(self.D_name)
        #I unsigned int ,...
        #packed=struct.pack("I%ds" % (len(s),), len(s), s)
        #pack = struct.Struct('s')
        #pack = struct.pack()
        #struct.pack("!2I100s", 0b1101, 0b0100, self.file_read)
        #This client program encodes an integer, a string of two characters, and a floating point value into a sequence of bytes that can be passed to the socket for transmission.
        #values = (1, 'ab', 2.7)
        #p_data = pack.pack(s)
        #print('sending', binascii.hexlify(packed))
        #print type (binascii.hexlify(packed))
        #print type(packed)
        if self.obj.protocol == 1:
                #toB = format(60000, "b")
                #self.obj.conn.send(toB)
                self.obj.conn.send(self.filename)
                #t2 = threading.Thread(target=P_fileT(self.obj.Ip, self.obj.protocol))
                #toB=binascii.hexlify(60000)
                #self.obj.sock.send(toB)
                #self.obj.sock.send('hi')
                #self.obj.conn.send(packed)
                #self.obj.Send_file(self.filename)
                print('file is sent')
                #t2 = threading.Thread(target=P_fileT(self.obj.Ip,self.obj.protocol))
        elif self.obj.protocol == 2:
                self.obj.conn.sendall(self.filename)
                print('file is sent')

    def Uploud_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="select File",
                                              filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*")))
        self.D_name=self.filename.split('/')[-1]
        self.label= Label(self.frame,text=self.D_name)
        self.label.grid(column=0,row=1)
        self.Cancel=Button(self.frame,text="Cancel", command=lambda:'')
        self.Cancel.grid(column=1,row=1)
#        self.update()
        self.obj.set_file_name(True)
        # send the file name .. at the reciever itwill appear with a download .. bool if file name is sent
        self.sending_file()


    def GetMsg(self):
        msg= self.T2.get("1.0",END)
        self.T.insert(END,(self.obj.Ip ,msg))
        #self.ToTextBox(msg)
        if self.obj.protocol ==1:
            self.obj.conn.send(msg.encode("UTF-8"))
        elif self.obj.protocol ==2:
            self.obj.sock.sendto(msg.encode("UTF-8"),(self.obj.Ip,self.obj.Port))
        #self.obj.conn.send(msg.encode(("utf-8")))
        print("message has been sent...")
        self.T2.delete('1.0', END)

    def ToTextBox(self,msg):
        self.T.insert(END,msg)


class emoji(Chat):
    def __init__(self,other, soc):
        self.other=other
        #self.T = Tk()
        self.frame = Frame()
        self.btn = Button(self.frame,text =u'\U0001F601' ,command=lambda: self.send(u'\U0001F601'))
        self.btn.grid(column=0,row=0)
        self.btn = Button(self.frame,text =u'\U0001F600',command=lambda: self.send(u'\U0001F600'))
        self.btn.grid(column=1,row=0)
        self.btn = Button(self.frame,text =u'\U0001F923',command=lambda: self.send(u'\U0001F923'))
        self.btn.grid(column=2,row=0)
        self.btn = Button(self.frame,text =u'\U0001F60E',command=lambda: self.send(u'\U0001F60E'))
        self.btn.grid(column=3,row=0)
        self.btn = Button(self.frame,text =u'\U0001f63b',command=lambda: self.send(u'\U0001f63b'))
        self.btn.grid(column=4,row=0)
        self.btn = Button(self.frame,text =u'\U0001F917',command=lambda:self.send(u'\U0001F917'))
        self.btn.grid(column=5,row=0)
        self.btn = Button(self.frame,text =u'\U0001F644', command=lambda:self.send(u'\U0001F644'))
        self.btn.grid(column=6,row=0)
        self.frame.grid()


    def send(self,em):
        self.other.T2.insert(END,em)
        #self.other.obj.conn.send(em.encode("utf-8"))
        print("message has been sent...")

class P_fileT():
    def __init__(self,D_ip,protocol):
        self.protocol = protocol
        self.isfilename=False
        if protocol==1:
            print(protocol)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.Ip =D_ip
            self.Port =  60000
            print ( 'starting up on ' , self.Ip)
            self.sock.bind((self.Ip,self.Port))
            self.sock.listen(1)
            self.conn, self.addr = self.sock.accept()
            print("connected to",self.addr)
            #you dont need the if statment
            t = threading.Thread(target=self.wait)
            t.start()


def main():
    app = Start ()

main()

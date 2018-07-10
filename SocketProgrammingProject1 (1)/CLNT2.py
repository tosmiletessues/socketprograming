from Tkinter import *
import socket
import threading
import tkFileDialog
import tkFileDialog as filedialog
import time
import random
import struct
import binascii


#import threading
import select, sys, Queue
class Head():
    def __init__(self):
        s = Start()

class Start(Head):
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
        self.btn = Button(self.frame,text="Start Connection=>",command=lambda: self.Start_connection())
        self.btn.grid(columnspan=3)
        self.label4= Label(self.frame,text="WATING FOR CONNECRION PARTNER",fg="red" ,font='bold' )
        self.label4.grid(columnspan=3)
        self.frame.grid()
        self.T.mainloop()

    def Start_connection(self):
        print(self.en.get())
        s= self.en.get().decode()
        print ('******',s.encode("utf-8"))
        s= client(s.encode("utf-8"),self.v.get())
        #C=Chat(s)


    def selected(self):
        print self.v.get()
        if self.v.get() == 1:
            print ("hi")
        elif self.v.get() ==2 :
            print("22222")

class Chat():
    print "here"
    def __init__(self,obj):
        self.obj=obj
        #self.T = Tk()
        #self.T.geometry('400x400')
        self.frame = Frame()
        #self.T.title("PyChatHost")
        self.T = Text(height=20, width=100)
        self.T.grid(column=0,row=0,sticky =W)
        self.T2 = Text(self.frame,height =7, width=50)
        self.T2.grid(column =0,row =2 , sticky = EW)
        self.btn = Button(self.frame,text="Send",command=lambda:self.GetMsg() )
        self.btn.grid(column=1,row =2)
        self.btn2= Button(self.frame, text="Emoji",command=lambda: emoji(self,obj))
        self.btn2.grid(column=2,row=2)
        self.Browse=Button(self.frame,text="Browse", command=lambda:self.Uploud_file())
        self.Browse.grid(column=3,row =2)
        self.frame.grid()
        #self.obj.Send_file()
    def Uploud_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="select File",
                                              filetypes=(("Excel Files", "*.xlsx"), ("All files", "*.*")))
        #self.obj.Send_file(filename)
        self.D_name = self.filename.split('/')[-1]
        self.label = Label(self.frame, text=self.D_name)
        self.label.grid(column=0, row=1)
        self.Cancel = Button(self.frame, text="Cancel", command=lambda: '')
        self.Cancel.grid(column=1, row=1)
        #self.update()
        self.obj.set_file_name(True)
        self.sending_file()
        # send file .. user must know file is comming
        #function that gets file directory and send to socket in binary
    # def file_to_send(self):
        # if(self.obj.protocol ==1):
        #     self.obj.sock.send(...) #all binary in while?
        #     self.obj.is_true(True)
        # elif self.obj.protocol==2:
        #     self.obj.sock.sendto((...), (self.obj.Ip, self.obj.Port))
        #     self.obj.is_true(True)
        # while True:
        #     skClient.send(sFileName)
        #     sData = skClient.recv(1024)
        #     fDownloadFile = open(sFileName, "wb")
        #     while sData:
        #         fDownloadFile.write(sData)
        #         sData = skClient.recv(1024)
        #     print "Download Completed"
        #     break
        #
        # skClient.close()

        ##update message status
        ##true value for file is sent .. send that to function or something
    def sending_file(self):
        #s = bytes(self.D_name)
        #I unsigned int ,...
        #pack=struct.pack("I%ds" % (len(s),), len(s), s)
        #pack = struct.Struct('s')
        #pack = struct.pack()
        #struct.pack("!2I100s", 0b1101, 0b0100, self.file_read)
        #This client program encodes an integer, a string of two characters, and a floating point value into a sequence of bytes that can be passed to the socket for transmission.
        #values = (1, 'ab', 2.7)
        #p_data = pack.pack(s)
        self.obj.sock.send(self.filename)
        #print('sending', binascii.hexlify(pack))
        if self.obj.protocol == 1:
                self.obj.sock.send(self.filename)
                #self.obj.Send_file(self.filename)
                print('file is sent')
        elif self.obj.protocol == 2:
                self.obj.sock.sendall(self.filename)
                print('file is sent')

    def GetMsg(self):
        msg = self.T2.get("1.0", END)
        self.T.insert(END,(self.obj.Ip,msg))
        # self.ToTextBox(msg)
        if self.obj.protocol == 1:
            self.obj.sock.send(msg.encode("UTF-8"))
        elif self.obj.protocol == 2:
            self.obj.sock.sendto(msg.encode("UTF-8"), (self.obj.Ip, self.obj.Port))
        # file or text?
        print("message has been sent...")
        self.T2.delete('1.0', END)


        #return msg






class emoji(Chat):
    def __init__(self,other,soc):
        self.other = other
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

class client (Chat):
    def dest_ip(self,ip,obj):
        self.D_ip = ip
        print ip

    def __init__(self,D_ip,protocol):
        self.protocol = protocol
        self.isfilename=False
        self.file_on = False
        if protocol==1:
            print(protocol)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            self.Ip=D_ip
            self.Port = 10000
            print ('connecting to  ' , self.Ip)
            self.sock.connect((self.Ip,self.Port))
            print ('connected to  ' ,( self.Ip,self.Port))
            self.C = Chat(self)
            t = threading.Thread(target=self.wait)
            t.start()

            # while 1:
            #     incoming_message = sock.recv(1024)
            #     incoming_message = incoming_message.decode()
            #     print(" Server : ", incoming_message)
            #     print("")
            #     message = input(str(">> "))
            #     # msg = T2.get()
            #     # print msg
            #     # message = message.encode()
            #     # self.s.send(msg)
            #     print("message has been sent...")
            #     print("")
        elif protocol == 2:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("happened")
            self.Ip = D_ip
            self.Port = 10000
            self.C=Chat(self)
            print("happened")
            #self.sock.sendto("Helllo", ('127.0.0.1', 10000))
            t = threading.Thread(target=self.wait)
            t.start()
    def flag_to_Send(self):
        self.saveAs = tkFileDialog.asksaveasfile(mode='w')
        if self.protocol == 1:
            self.sock.send('/send-file/')
            self.file_on = True
            print self.file_on
        elif self.protocol == 2:
            self.sock.send('/send-file/')
            self.file_on = True
            print self.file_on

    def wait(self):
        print('called')

        while (True):
            if self.protocol == 1:
                self.data = self.sock.recv(1024)
                self.expected_sequence_number = 0
                self.prev = ""

                #self.sock.send(self.data.encode("utf-8"))
                print self.file_on
                if self.file_on == True:
                    #self.sock.settimeout(4)
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
                            self.sock.send('Ack')
                            text2save, received_sequence_number = self.parse_message(self.data)
                            self.prev = self.data
                            self.expected_sequence_number = received_sequence_number

                            print text2save, received_sequence_number
                        else:
                            print " duplicated message: " + text2save

                        if (received_sequence_number == self.expected_sequence_number):
                            print(text2save)
                            print
                            self.saveAs.write(text2save)
                            print ('right')
                            # self.conn.send('Ack')
                            self.expected_sequence_number = received_sequence_number + 1
                        elif received_sequence_number != self.expected_sequence_number:
                            print ('Error .. not in order')
                            # self.conn.send("Bad ACK")
                            continue

                            # choice = random.randint(1, 4)
                            #
                            # if choice == 1:
                            #     client.send(str(received_sequence_number))
                            #     print "Receiver responds with ACK " + str(received_sequence_number)
                            #     expected_sequence_number = self.NACK(expected_sequence_number)
                            #     continue
                            # elif choice == 2:
                            #     client.send("Bad ACK")
                            #     print "A corrupted ACK is sent"
                            #     continue
                            # elif choice == 3:
                            #     print "Receiver does not send ACK"
                            #     continue
                            # else:
                            #     client.send(str(self.NACK(received_sequence_number)))
                            #     print "incorrectly responds with ACK " + str(self.NACK(received_sequence_number))
                            #     continue

                        print(text2save)
                        self.saveAs.write(text2save)


                        print (text2save)
                        print('saw that')

                        # close file when file_on==false
                        #if you reciev a certain thing the stream is over..close
                else:
                    if 'C:/' in self.data :
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

                    else:
                        self.C.T.insert(END, (self.Ip, ": ", self.data.decode("UTF-8")))
                        print self.data
                    #print self.adr
                    #self.data, self.adr = self.sock.recv(1024)
            elif self.protocol == 2:
                    self.data, self.addr = self.sock.recvfrom(1000)
                    if self.file_on == True:
                        print('TRue')
                        print ('here?')
                        if '/-end-/' in self.data:
                            print('closed')
                            self.saveAs.close()
                            self.file_on = False
                        else:
                            text2save = self.data
                            print(text2save)
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

    def parse_message(self,message):
        if message == "":
            return None
        list_message = message.split()
        data = message[:-1]
        received_sequence_number = int(list_message[-1])
        print data, received_sequence_number
        return data, received_sequence_number

        #self.sock.bind((self.Ip, 10000))
                #self.sock.sendto(self.data.encode("utf-8"), (self.Ip, self.Port))


            #self.sock.sendto(C.GetMsg().encode("utf-8"),(self.Ip,self.Port))
            #C.T.insert(END,(self.Ip, ": " ,C.GetMsg().encode("utf-8")))
            #data,add=self.sock.recvfrom(1024)
            #reply=d[0]
            #addr=d[1]
            #self.sock.bind((self.Ip, self.Port))
            #print(add)
            # while True:
            #     data, addr = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
            #     print "received message:", data
            # # #try:
            #     # Send data
            #     message = 'This is the message.  It will be repeated.'
            #     print >> sys.stderr, 'sending "%s"' % message
            #     sock.sendall(message)
            #
            #     # Look for the response
            #     amount_received = 0
            #     amount_expected = len(message)
            #
            #     while amount_received < amount_expected:
            #         data = self.sock.recv(1024)
            #         amount_received += len(data)
            #         print ( sys.stderr, 'received "%s"' % data)
            # finally:
            #     print >> sys.stderr, 'closing socket'
            #     sock.close()
            # #self.s = socket.socket()
        #     self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #     Ip_Port = (D_ip, 10000)
        #     #print >> sys.stderr, 'starting up on %s port %s' % server_address
        #     self.sock.bind(Ip_Port)
        #     self.sock.listen(1)
        #     while True:
        #     # Wait for a connection
        #         print >> sys.stderr, 'waiting for a connection'
        #         self.conn, self.address = self.sock.accept()
        #     print(self.address, " Has connected to the server and is now online ...")
        #     C = Chat(self)
        #     try:
        #         print >> sys.stderr, 'connection from', client_address
        #
        #         # Receive the data in small chunks and retransmit it
        #         while True:
        #             data = connection.recv(1024)
        #             print( sys.stderr, 'received "%s"' % data)
        #             if data:
        #                 print (sys.stderr, 'sending data back to the client')
        #                 connection.sendall(data)
        #             else:
        #                 print ( sys.stderr, 'no more data from', client_address)
        #                 break
        #     finally:
        #     # Clean up the connection
        #         connection.close()
        # #
        # self.s = socket.socket()
        # host = D_ip
        # port = 10000
        # print D_ip
        # print (type(D_ip))
        # print (host, port)
        # self.s.connect((host, port))
        # C = Chat(self)
        # print(" Connected to chat server")
        # i = 1
        # while i==1:
        #     incoming_message = self.s.recv(1024)
        #     incoming_message = incoming_message.decode()
        #     print(" Server : ", incoming_message)
        #     print("")
        #     message = input(str(">> "))
        #     #msg = T2.get()
        #     #print msg
        #     #message = message.encode()
        #     #self.s.send(msg)
        #     print("message has been sent...")
        #     print("")
        #     i=i-1


    def on_transm(self,filename):
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

    def NACK(number):
        return 0 if number else 1

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
                    try:
                        self.data= self.sock.recv(1024)
                    except socket.timeout:
                        print('Time_out')
                        self.send_file([i])
                        continue
                    else:
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
                    #self.start = time.time()
                    self.sequence_number+=1
                    if self.sequence_number== 9:
                        self.sequence_number=0
                #t = threading.Thread(target=self.wait_before_sending())
                #t.start()
                print ('done')
                self.sock.send('/-end-/')

        elif self.protocol ==2:
            for i in packets:
                mesg = i + " " + str(self.sequence_number)  # assemble message as a string
                self.send_pack(self, mesg)
                self.sequence_number+=1
                self.start = time.time()
                #t = threading.Thread(target=self.wait_before_sending())
                print ('done')
            self.sock.send('/-end-/')

    def wait_before_sending(self):
  # socket timeout

        while True:
            if time.time() - self.start < 4:
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
            self.sock.send(pack)
        elif self.protocol ==2:
            self.sock.send(pack)
    def File_on(self,value):
        self.file_on=True
    def File_off(self,value):
        self.file_on=False
    def get_value(self):
        return self.file_on

    def Msg(self,msg):
        print msg

    def sentmsg(self,msg):
        self.msg = msg

    def file_name(self):
        return self.isfilename

    def is_file(self):

        return

    def set_file_name(self, value):
        self.isfilename=value

    def set_is_file(self, value):
        return value

class FileServer(Chat):
    def __init__(self, soc,other):
        self.protocol = soc.protocol
        self.isfilename = False
        if self.protocol == 1:
            print(self.protocol)
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Connect the socket to the port where the server is listening
            self.Ip = soc.D_ip
            self.Port = 10000
            print ('connecting to  ', self.Ip)
            self.sock.connect((self.Ip, self.Port))
            print ('connected to  ', (self.Ip, self.Port))
            self.C = Chat(self)
            t = threading.Thread(target=self.wait)
            t.start()

    # def Send_file(self, file):
    #     # DownloadFile = open('vclient.txt', "wb")
    #     # sData = ''
    #     # # DOWNLOAD OR UPLOUD?
    #     # print('gon start')
    #     # while sData:
    #     #         DownloadFile.write(sData)
    #     #         sData = self.sock.recv(1024)
    #     #         print('got it')
    #     #         print sData
    #     # print "Download Completed"
    #     #
    #     UploadFile = open(file, "rb")
    #     sRead = UploadFile.read(1024)
    #     while sRead:
    #         print sRead
    #         self.sock.send(sRead)
    #         sRead = UploadFile.read(1024)
    #     print "Sending Completed"
# while True:
#     skClient.send(sFileName)
#     sData = skClient.recv(1024)
#     fDownloadFile = open(sFileName, "wb")
#     while sData:
#         fDownloadFile.write(sData)
#         sData = skClient.recv(1024)
#     print "Download Completed"
#     break
#
# skClient.close()

def main():
    #s = Socket()
    #app = Start ()
    app= Head()

main()


import datetime
import socket
import sys
from threading import Thread
import random
from time import sleep
from typing import Callable
from .channels import StringChannel



class Host:
    __channels=dict()

    def __init__(self) -> None:
        self.__port=random.Random().randint(8000,15000)
        
        _LogChannel.oldStd.write(str(self.__port))
        self.__server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    
        self.__server.bind(('127.0.0.1',self.__port))
        Thread(target= self.__startListen).start()
        if 'dart' in sys.argv:
            self.debugChannel=StringChannel('|debug|') 
            self.bindChannel(self.debugChannel)
            sys.stdout=_LogChannel(self.debugChannel)
            self.controller=_controlChannel(self.debugChannel,self.__server)
    def __startListen(self):
        self.__server.listen()
      
        while True:
            try:
                conn,addr=self.__server.accept()
            except :
                break
            while True:
                
                buffer=conn.recv(1024)
                if bytes([0,0,0]) in buffer:
                    index=buffer.index((bytes([0,0,0])))
                    channelName=buffer[0:index]
        
                    channelName=channelName.decode('utf-8')
         
                    if channelName in self.__channels:

                        Thread(target=self.__channels[channelName].setConnection,args=(conn,buffer)).start()
                    break
    def setOnDisconnect(self,callback:Callable):
        self.debugChannel.setOnDisconnect(callback)
       
    def bindChannel(self,channel):
        self.__channels[channel.name]=channel
  



class _LogChannel:
    oldStd=None
    def __init__(self,channel=None) -> None:
        self.channel=channel
    
    def write(self,log):
        if self.channel:
            self.channel.send(log)
    
    def flush(self):
        self.oldStd.flush()
def setStdout():
    _LogChannel.oldStd=sys.stdout
    if 'dart' in sys.argv:
        sys.stdout=_LogChannel()

class _controlChannel:

    def __init__(self,channel,server:socket.socket) -> None:
        self.__channel=channel
        self.__server=server
        self.lastMsg=datetime.datetime.now()
        self.__channel.setHandler(self.__handler)
        
        self.th=Thread(target=self.__checkOnConnect)
        self.th.start()
    def __checkOnConnect(self): 
      
        while True: 
            if (datetime.datetime.now()-self.lastMsg).seconds >10:
                self.__server.close()
                
                break
            sleep(1)
    def __handler(self,msg,r):
        self.lastMsg=datetime.datetime.now()









setStdout()



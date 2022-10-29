import socket
from threading import Thread
import random

class Host:
    __channels=dict()
    def __init__(self) -> None:
        self.__port=random.Random().randint(8000,15000)
        print(self.__port)
        self.server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind(('127.0.0.1',self.__port))
        Thread(target= self.__startListen).start()

    def __startListen(self):
        self.server.listen()
        while True:
            conn,addr=self.server.accept()
            while True:
                
                buffer=conn.recv(1024)
                if bytes([0,0,0]) in buffer:
                    index=buffer.index((bytes([0,0,0])))
                    channelName=buffer[0:index]
        
                    channelName=channelName.decode('utf-8')
                    if channelName in self.__channels:
                        
                        Thread(target=self.__channels[channelName].setConnection,args=(conn,buffer)).start()
                    break
           

    def bindChannel(self,channel):
        self.__channels[channel.name]=channel
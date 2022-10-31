from multiprocessing import Queue
from threading import Thread,Event
from time import sleep
from socket import socket
from .reply import Reply
from typing import Callable
from utils.boradcast import GeneratorBroadcast
from message import Message
import random
import json
class Channel:
    
    
    def __init__(self,name:str):
        self.name=name        
        self.awaitMessages=[]
        self.__handeler=None
        self.connection:socket=None
        self.broadcast:GeneratorBroadcast=None    
        
    def setConnection(self,connection:socket,buffer):
        # print(self.name)
        self.connection=connection
        self.broadcast=GeneratorBroadcast(self.__listenToSocket(buffer))
        self.broadcast.addCallback(self.__listenToMessages,self.broadcast.genID())
        self.broadcast.startBroadcast()
        while self.awaitMessages:
            msg=self.awaitMessages[0]
            self.awaitMessages.remove(msg)
            self.send(msg['data'],msg['callback'])
    def __listenToSocket(self,buffer):
        buffer=buffer[:]
        q=Queue()
        # remove chanel name msg
        index=buffer.index((bytes([0,0,0])))
        buffer=buffer[index+3:]
        
        
        event=Event()
        def listen(queue:Queue):
            while True:        
                data=self.connection.recv(1024)
                if not data:
                    event.set()
                    break
                queue.put(data)
        Thread(target=listen,args=(q,)).start()
        
        while not event.isSet() or buffer:
            if not q.empty():
                buffer+=q.get_nowait()
            if bytes([0,0,0]) in buffer:
                index=buffer.index((bytes([0,0,0])))
                msg=buffer[5:index]
                msgID=buffer[0:4]
                msgID=self.__int_from_bytes(msgID)
                yield Message(data=msg,id=msgID,isReply=buffer[4]==1)
                buffer=buffer[index+3:]
            sleep(0.1)
                    

    def genID(self):
        
        r=random.Random().randint(16777216,4294967295)
        return self.__int_to_bytes(r)

    def __listenToMessages(self,msg:Message):
        if not msg.isReply:
            reply= Reply(self,msg.id)
            if not self.__handeler is None:
                self.__handeler(self.encode(msg.data),reply)
        


    def __int_to_bytes(self,value: int) -> bytes:
        bin=[]
        while not value==0:
            bin.append(value % 2)
            value=int(value / 2)
        bin+=[0]*(32-len(bin))
        bytesB=[bin[i * 8:(i + 1) * 8] for i in range(4)]
        bytesList=[]
        for byte in bytesB:
            sum=0
            pos=0
            for bit in byte:
                sum+=bit * pow(2,pos)
                pos+=1
            bytesList.append(int(sum))
        return bytes(bytesList)    
    def __int_from_bytes(self,bytes: bytes) -> int:
        
        bin=[]
        for b in bytes: 
            rb=8
            while not b==0:
                bin.append(b % 2)
                b=int(b/2)
                rb-=1
            bin+=[0]*rb
        sum=0
        pos=0
        for bit in bin:
            sum+=bit * pow(2,pos)
            pos+=1
        return int(sum) 

    def setHandeler(self,handeler:Callable[[bytes,Reply],None]):
        self.__handeler=handeler
    


    def send(self,data:bytes,callback:Callable[[bytes],None]|None=None):
 
        if not self.connection is None:
            id=self.genID()
            callbackID=self.broadcast.genID()
            if callback is not None:
                def _callback(msg:Message):
                    if msg.isReply and msg.id==self.__int_from_bytes(id): 
                        callback(self.encode(msg.data) if len(msg.data) else None)
                        self.broadcast.removeCallback(callbackID)
                self.broadcast.addCallback(_callback,callbackID)
            dd=self.decode(data)
            self.connection.sendall(id+bytes([0])+dd+bytes([0,0,0]))
        else:
            self.awaitMessages.append({"data":data,'callback':callback})

    def sendReply(self,data:bytes|None,msgID:int):
        if not self.connection is None:
            
            self.connection.sendall(self.__int_to_bytes(msgID)+bytes([1])+(self.decode(data) if data else bytes([]))+bytes([0,0,0]))
    

class BytesChannel(Channel):
    
    def encode(self,data:bytes)->bytes: 
        return data
    def decode(self,data)->bytes: 
        return data


import json
from typing import Any, Callable
from .__channel import Channel
from ..methodCall import MethodCall
from ..exceptions import PythonChannelMethodException
from ..message import Message
from ..reply import Reply
class MethodChannel(Channel):

    def encodeInput(self,data:bytes):    
        jsStr=data.decode('utf-8')
        return MethodCall.fromJson(jsStr)
    def decodeInput(self,data:MethodCall)->bytes: 
        jsStr= data.toJson()
        return jsStr.encode('utf-8')
    def encodeOutput(self,data:bytes):    
        jsStr=data[1:].decode('utf-8')
        jsData=json.loads(jsStr)
        return jsData['value']
    def decodeOutput(self,data)->bytes: 
        jsData={'value':data}
        jsStr=json.dumps(jsData)
        return bytes([0])+jsStr.encode('utf-8')

    def encodeException(self, data: bytes):
        js=data[1:].decode('utf-8')
        return PythonChannelMethodException.fromJson(js)
    def decodeException(self, data: PythonChannelMethodException):
        js=data.toJson()
        return bytes([1])+js.encode('utf-8')
    
    
    def _listenToMessages(self,msg:Message):
        if not msg.isReply:
            reply= Reply(self,msg.id)
            if not self._handler is None:
                try:
                    self._handler(self.encodeInput(msg.data),reply)
                except PythonChannelMethodException as e:
                    self.__sendException(e,msg.id)
    def __sendException(self,data,msgID:int):
        if not self.connection is None:
            
            self.connection.sendall(self._int_to_bytes(msgID)+bytes([1])+(self.decodeException(data) if data else bytes([]))+bytes([0,0,0]))

    def invokeMethod(self,method:str,args:list|dict,callback:Callable[[bytes],None]|None=None):
        call =MethodCall(method,args)
        self.send(call,callback)
        

    def send(self,data:MethodCall,callback:Callable[[Any,PythonChannelMethodException],None]|None=None):
 
        if not self.connection is None:
            id=self.genID()
            callbackID=self.broadcast.genID()
            if callback is not None:
                def _callback(msg:Message):
                    if msg.isReply and msg.id==self._int_from_bytes(id):
                        if msg.data[0]==1:
         
                            callback(None,self.encodeException(msg.data))
                        else:
                            callback(self.encodeOutput(msg.data) if len(msg.data) else None,None)
                        self.broadcast.removeCallback(callbackID)
                self.broadcast.addCallback(_callback,callbackID)
            dd=self.decodeInput(data)
            self.connection.sendall(id+bytes([0])+dd+bytes([0,0,0]))
        else:
            self.awaitMessages.append({"data":data,'callback':callback})


from channels.__channel import Channel
from typing import Callable
class StringChannel(Channel):

    
    def encodeInput(self,data:bytes)->str: 
        return data.decode('utf-8')
    def decodeInput(self,data:str)->bytes: 
        return data.encode('utf-8')
    def encodeOutput(self,data:bytes)->str: 
        return data.decode('utf-8')
    def decodeOutput(self,data:str)->bytes: 
        return data.encode('utf-8')
        
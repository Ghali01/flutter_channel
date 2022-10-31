from channels.channel import Channel
from typing import Callable
class StringChannel(Channel):

    
    def encode(self,data:bytes)->str: 
        return data.decode('utf-8')
    def decode(self,data:str)->bytes: 
        from channels import debugChannel
        return data.encode('utf-8')
    # def send(self,data:str,callback:Callable[[str],None]|None=None):
    #     super().send(data,callback)
    # def sendReply(self,data:str|None,msgID:int):
    #     super().sendReply(data,msgID)
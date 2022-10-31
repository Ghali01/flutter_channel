from channels.channel import Channel
from typing import Callable
import json
class JsonChannel(Channel):

    
    def encode(self,data:bytes)->dict|list: 
        js= data.decode('utf-8')
        
        return json.loads(js)
    def decode(self,data:dict|list)->bytes: 
        js=json.dumps(data)
        return js.encode('utf-8')
    # def send(self,data:dict|list,callback:Callable[[dict|list],None]|None=None):
    #     from channels import debugChannel
    #     debugChannel.send(f'jc16 {type(super())}')
    #     super(JsonChannel,self).send(data,callback)
    # def sendReply(self,data:dict|list|None,msgID:int):
    #     super(JsonChannel,self).sendReply(data,msgID)   


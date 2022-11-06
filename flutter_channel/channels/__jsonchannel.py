from .__channel import Channel
from typing import Callable
import json
class JsonChannel(Channel):

    
    def encodeInput(self,data:bytes)->dict|list: 
        js= data.decode('utf-8')
        
        return json.loads(js)
    def decodeInput(self,data:dict|list)->bytes: 
        js=json.dumps(data)
        return js.encode('utf-8')


    
    def encodeOutput(self,data:bytes)->dict|list: 
        js= data.decode('utf-8')
        
        return json.loads(js)
    def decodeOutput(self,data:dict|list)->bytes: 
        js=json.dumps(data)
        return js.encode('utf-8')


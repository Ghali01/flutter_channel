from .exceptions import ArgsMethodCallException
import json
class MethodCall:

    def __init__(self,method:str,args:dict|list) -> None:
        # if not (args is dict or args is list):
        #     raise ArgsMethodCallException()
        self.method=method
        self.args=args

    def toDict(self)->dict: 
        return {
            "method":self.method,
            "args":self.args
        }
    @staticmethod
    def fromMap(data:dict): 
        return MethodCall(**data)

    def toJson(self)->str:
        return json.dumps(self.toDict())
    
    @staticmethod
    def fromJson(jsonStr):
        return MethodCall.fromMap(json.loads(jsonStr))
    

    def __str__(self) -> str:
        return self.toJson()
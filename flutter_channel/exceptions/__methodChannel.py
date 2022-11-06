from dataclasses import dataclass
import json

class ArgsMethodCallException(Exception):


    def __str__(self) -> str:
        return 'MehtodCall args should be list or dict'

@dataclass
class PythonChannelMethodException(Exception):
    code:int 
    message:str
    details:str

    def toDict(self):    
        return {
            'code':self.code,
            'message':self.message,
            'details':self.details
        }
    def toJson(self):
        return json.dumps(self.toDict())

    @staticmethod
    def fromDict(data:dict):
        return PythonChannelMethodException(**data)

    @staticmethod
    def fromJson(data:str):
        return PythonChannelMethodException.fromDict(json.loads(data))
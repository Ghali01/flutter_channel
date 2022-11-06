from dataclasses import dataclass

@dataclass
class Message:
    data:bytes|None
    id:int
    isReply:bool
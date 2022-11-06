import threading
import typing
import random
class GeneratorBroadcast:
    def __init__(self,generator:typing.Iterable) -> None:
        self.generator=None
        self.__callbacks=dict()
        self.generator=generator

    def genID(self):
        rand=random.Random()
        id=rand.randint(1,100000)
        while id in self.__callbacks:
            id=rand.randint(1,100000)
        return id
    def addCallback(self,callback:typing.Callable[[typing.Any],None],id:int):
        
        self.__callbacks[id]=callback
    def removeCallback(self,id:int):
        del self.__callbacks[id]


    def startBroadcast(self):
        def broadcast():
            for el in self.generator:
                for callback in list(self.__callbacks.values()):
                    threading.Thread(target=callback,args=(el,)).start()
        threading.Thread(target=broadcast).start()
        
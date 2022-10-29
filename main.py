import threading
from host import Host
from channels.channel import BytesChannel,debugCh
from time import sleep
import sys

def handeler(ch,msg,reply):
    debugCh.send(b'python got '+msg)
   
    reply.reply(None)

def main():
    host=Host()
    
    # sys.stdout=open('E:\\projects\\python_channel\\flutter_channel\\debug.txt','w')
    # print('hi')
    ch1=BytesChannel('ch1')
    ch1.setHandeler(lambda  d,r:handeler('ch1',d,r))
    
    ch2=BytesChannel('ch2')
    ch2.setHandeler(lambda  d,r:handeler('ch2',d,r))
    host.bindChannel(ch1)
    host.bindChannel(ch2)
    host.bindChannel(debugCh)
    def dd(d):
        if d:
            debugCh.send(b'python got reply'+d)
        else:
            debugCh.send(b'python got reply None')
    ch1.send(b'hello world from python',dd)
if __name__=='__main__':
    main()
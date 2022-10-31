import threading
from channels import BytesChannel,JsonChannel, StringChannel,debugChannel
from host import Host
from time import sleep
import sys

def handeler(msg,reply):
    debugChannel.send(f'python got {msg}')
    reply.reply(None)

def main():
    host=Host()
    ch=JsonChannel('ch')
    
    host.bindChannel(ch)
    ch.setHandeler(handeler)
    ch.send({"key":True})    
    ch2=StringChannel('ch2')
    ch2.setHandeler(handeler)
    host.bindChannel(ch2)
    ch2.send('test')
    
    
if __name__=='__main__':
    main() 
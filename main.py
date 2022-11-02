import threading
from channels import BytesChannel,JsonChannel, StringChannel,MethodChannel
from host import Host
from methodCall import MethodCall
from exceptions import PythonChannelMethodExcetption
def handeler(msg,reply):
    raise PythonChannelMethodExcetption(100,'msg','txt')
    print(f'python got {msg}')    
    if msg.method=='add':
        reply.reply(add(msg.args[0],msg.args[1],))
    return
    reply.reply(None)

def add(n1,n2):
    return n1+n2

def main():
    
    host=Host()
    ch=MethodChannel('ch')
    ch.setHandeler(handeler)
    host.bindChannel(ch)
    
if __name__=='__main__':
    main() 
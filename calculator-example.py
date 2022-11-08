from flutter_channel.channels import  MethodChannel
from flutter_channel.host import Host
from flutter_channel.exceptions import PythonChannelMethodException
def handler(msg,reply):
    if msg.method=='add':
        reply.reply(add(msg.args[0],msg.args[1],))
    if msg.method=='sub':
        reply.reply(sub(msg.args[0],msg.args[1],))

    if msg.method=='mul':
        reply.reply(mul(msg.args[0],msg.args[1],))

    if msg.method=='div':
        reply.reply(div(msg.args[0],msg.args[1],))
    else:
        raise PythonChannelMethodException(404,'method not found','method not found')
def add(n1,n2):
    return n1+n2
def sub(n1,n2):
    return n1-n2
def mul(n1,n2):
    return n1*n2
def div(n1,n2):
    return n1/n2

def main():
    
    host=Host()
    channel=MethodChannel('ch')
    host.bindChannel(channel)
    channel.setHandler(handler)
    
    
if __name__=='__main__':
    main() 


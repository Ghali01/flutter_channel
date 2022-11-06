import threading
from flutter_channel.channels import  BytesChannel,JsonChannel, StringChannel,MethodChannel
from flutter_channel.host import Host
from flutter_channel.methodCall import MethodCall
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
    from flutter_channel.channels import BytesChannel,JsonChannel, StringChannel,MethodChannel
    bytesChannel=BytesChannel('channel1')
    stringChannel=StringChannel('channel2')
    jsonChannel=JsonChannel('channel3')
    methodChannel=MethodChannel('channel4')
    def callBack(replyMessage):
        pass
    bytesChannel.send(bytes([1,1,4,5]),callBack)
    stringChannel.send('hello world',callBack)
    jsonChannel.send({"hello":"world"},callBack)
    def callBackMethod(replyMessage,exception):
        pass

    methodChannel.send(MethodCall(method='sayHello',args={"name":'ghale'}),callBackMethod)
    # or
    methodChannel.invokeMethod(method='sayHello',args={"name":'ghale'},callback=callBackMethod)
if __name__=='__main__':
    main() 
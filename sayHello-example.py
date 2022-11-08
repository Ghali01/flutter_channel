from flutter_channel import Host
from flutter_channel.channels import MethodChannel
from flutter_channel.exceptions import PythonChannelMethodException
def handler(msg,reply):
    
    if msg.method=='sayHello':
        reply.reply(f'hi {msg.args["name"]}')
    else:
        raise PythonChannelMethodException(404,'method not found','method not found')


def main():
    host=Host()
    channel=MethodChannel('sayHi')
    channel.setHandler(handler)
    host.bindChannel(channel)
if __name__=='__main__':
    main()
# flutter_channel

With this package developers can use python in there flutter applications on windows.

## how does it work?

This package depends on unix sockets (TCP) protocol.

## how to use?

### 1. create host

You have to create instance from `Host` class to use it in channels binding as following:

```py
    from flutter_channel.host import Host
    host=Host()
```

### 2. create channels and bind it

There is number of built in channel types to use like:  `BytesChannel`,`JsonChannel`, `StringChannel` and `MethodChannel`.

```py
from flutter_channel.channels import BytesChannel,JsonChannel, StringChannel,MethodChannel
channel1=BytesChannel('channel1')
channel2=StringChannel('channel2')
channel3=JsonChannel('channel3')
channel4=MethodChannel('channel4')
host.bindChannel(channel1)
host.bindChannel(channel2)
host.bindChannel(channel3)
host.bindChannel(channel4)
```

### 3. set channel handler  

The handler of the channel is a function that receive the messages that is sent to the channel, Each handler should take tow parameters `message` and `reply`.

`message`  is the first parameter and it is the massage that was received and it's type depends on the channel type see the following table.

| Channel Type | Channel Output |
|:---:|:---:|
| `BytesChannel` | `bytes` |
| `StringChannel` | `str` |
| `JsonChannel` | `dict` or `list` |
| `MethodChannel` | depends on reply that comes from dart can be any primitive type like `int` ,`str`,`bool` or `list`   |
| custom channel | depends on the implement of the `encodeOutput` and `decodeOutput` methods |

`reply` is the second parameter, it is instance of `Reply` you should use this object to send reply on the received message, You can reply with another message or reply with `None`.
Your reply will not be sent to the channel handler in the dart side. It will be send to the `send` Future that sent the original message.

 **You have to send reply otherwise dart `Future` will not complete**

#### example 1

```py
def handler(msg,reply):
    # do some logic
    reply.reply(None)
channel.setHandler(handler)
```

#### example 2

```py
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
    methodChannel.setHandler(handler)
```

### send message

You can send message to dart side using `send(message,callback)` method where `message` type depends on the channel type  see the following table and `callback` is a function that will be invoked when reply comes back from dart and it take one parameter present the reply message.

| Channel Type | Channel input |
|:---:|:---:|
| `BytesChannel` | `bytes` |
| `StringChannel` | `str` |
| `JsonChannel` | `dict` or `list` |
| `MethodChannel` | `MethodCall` |
| custom channel | depends on the implement of the `encodeInput` and `decodeInput` methods |

#### examples

```py
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
```

### MethodChannel

There is some notes we have to mention to about MethodChannel usage.

#### 1. the handler

The handler of the `MethodChannel` receive two parameter first one is `MethodCall` instance and second one is `Reply` instance.

#### 2. the reply callback

the reply callback function take two parameter, First one is the reply message and the second on is exception with `PythonChannelMethodException` type if exception raised in dart side otherwise the parameter will be `None`.

#### 3. raise exception in the handler

You can raise `PythonChannelMethodException` in the handler this exception will be sent by the channel and will throw it to the `send` Future in dart side.

##### example

```python

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
```

## print() function

This package change the behavior of the `print()` the stdout of the python will be the debug console of the flutter
**Note: you should't use `print` before create `Host` instance**

## create your own channel type

You can create your own channel by write class that inherit `Channel` class.
You should implement 4 method `encodeInput`, `encodeOutput` ,`decodeInput` and `decodeOutput`

+ `encodeInput` convert the input of the channel from `bytes`
+ `encodeOutput` convert the output of the channel from `bytes`
+ `decodeInput` convert the input of the channel to `bytes`
+ `decodeOutput` convert the input of the channel to `bytes`
where the **input** is what the channel send and the **output** is what the channel receive

### for example

```py
    from flutter_channel.channels import Channel,
    class StringChannel(Channel):
    
    def encodeInput(self,data:bytes)->str: 
        return data.decode('utf-8')
    def decodeInput(self,data:str)->bytes: 
        return data.encode('utf-8')
    def encodeOutput(self,data:bytes)->str: 
        return data.decode('utf-8')
    def decodeOutput(self,data:str)->bytes: 
        return data.encode('utf-8')
```

## release mode

in release mode you have to compile you main python file to an executable file, We recommend you to use [PyInstaller](https://pypi.org/project/pyinstaller/).
**Note: you have to build the executable file with console otherwise the package will not work**

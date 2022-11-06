

class Reply:


    def __init__(self,channel,msgID):
        self.channel=channel
        self.msgID=msgID

    def reply(self,data): 
            self.channel.sendReply(data,self.msgID)
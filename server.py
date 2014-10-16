from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
 
class iPhoneChat(Protocol):
    
    def connectionMade(self):
    	# EFFECTS:	Handles the event where a connection is created.
    	self.factory.clients.append(self)
        print "clients are ", self.factory.clients
    
    def connectionLost(self, reason):
    	# EFFECTS:	Handles the event where a connection is lost.
    	print reason
    	self.factory.clients.remove(self)

    def dataReceived(self, data):
    	# EFFECTS:	Handles when a client sends data.
        data = data[0:len(data)]
    	messages = data.split(":")

    	if len(messages) > 1:
    		command = messages[0]
    		content = messages[1]

    		msg = ""

    		# Client joined
    		if command == "iam":
    			self.name = content
    			print self.name, "has joined!"

			# Client sent message
    		elif command == "msg":
    			msg = self.name + ": " + content
    			print msg

    			# Send message to all clients
                for client in self.factory.clients:
                    if client != self:
                        client.message(msg)

    def message(self, msg):
    # EFFECTS:	Sends a message to a the client.
    	self.transport.write(msg + '\n')
 
factory = Factory()
factory.protocol = iPhoneChat
factory.clients = []

reactor.listenTCP(8081, factory)
print "iPhone chat server started!"
reactor.run()
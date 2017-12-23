from autobahn.twisted.websocket import WebSocketServerProtocol

class MyServerProtocol(WebSocketServerProtocol):

   def onMessage(self, payload, isBinary):
      ## echo back message verbatim
      self.sendMessage(payload, isBinary)
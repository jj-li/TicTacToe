#import socket module
#Jia Li 109843894
from socket import *
import select, uuid, board, jaw_enums, json
#import player

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverPort = 9347
serverSocket.bind(('', serverPort))
serverSocket.listen(1)
serverSocket.setblocking(0)

epoll = select.epoll()
epoll.register(serverSocket.fileno(), select.EPOLLIN)

class Server(object):
	def __init__(self):
		self.players = {}
		self.games = {}
		self.connections = {}

	'''main methods''' 
	def addConnection(self, connection):
		'''
		Add connection new socket connection
		@param connection the new socket connection
		'''
		self.connections[connection.fileno()] = connection

	def playerAvailable(self, username):
		'''
		Checks if player with a user id of username is busy or not
		@param username User id of user to check for
		@return True if player is not busy. False otherwise.
		'''
		for key, value in self.players.iteritems():
			if username == value.username:
				return value.status
		return False

	def playerExists(self, username):
		'''
		Checks if player with a user id of username exists
		@param username User id of user to check for
		@return True if player exists. False otherwise.
		'''
		for key, value in self.players.iteritems():
			if username == value.username:
				return True
		return False

	def getAvailablePlayers(self):
		'''
		Returns the list of all available players
		@return List of all available players
		'''
		names = []
		for key, value in self.players.iteritems():
			if value.status == True:
				names.append(value.username)
		return names

	def removePlayer(self, username):
		'''
		Removes the player with a user id of username
		@param usernamed User id of user to remove
		'''
		for key, value in self.players.iteritems():
			if username == value.username:
				#close connection and remove user
				return
		return

	def addPlayer(self, connection, player):
		'''
		Adds player to the server
		@param connection Socket connection associated with player
		@param player Player to add to the server
		'''
		self.players[connection.fileno()] = player

	def createGame(self, connection, p1, p2):
		'''
		Create game with 2 players
		@param connection Connection associated with p1 or p2
		@param p1 Player 1
		@param p2 Player 2
		'''
		gameId = uuid.uuid4().hex
		newBoard = None
		if p1.timeLoggedIn <= p2.timeLoggedIn:
			newBoard = Board(p1, p2, p1)
		else:
			newBoard = Board(p1, p2, p2)
		self.games[gameId] = newBoard
		p1.gameId = gameId
		p2.gameId = gameId
		return

	def endGame(self, gameID):
		'''
		Ends the game
		@param gameID Game ID of the game to end
		'''
		return

	def sendMessage(self, message, connection):
		'''
		Sends a message to the client
		@param message Message to send
		@param connection Sockwt connection to send message to
		'''
		connections[connection.fileno()].send("message")
		epoll.modify(connection.fileno(), 0)
		return


	def broadcast(self, message, connections):
		'''
		Broadcasts message to everyone
		@param message Message to send
		@param connections Socket connections to send message to
		'''
		for c in connections:
			sendMessage(message, c)


	def checkRequestProtocol(self, fileno):
		'''
		Checks the request protocol
		@param fileno Incoming socket connection file descriptor
		'''
		connection = self.connections[fileno]
		request = self.connections[fileno].recv(1024)
		recurr = request.count('\r\n\r\n')
		if recurr == 0 or recurr > 1:
			sendMessage("JAW/1.0 400 ERROR \r\n", connection)
			epoll.modify(fileno, select.EPOLLOUT)
			return
		request = request.split()
		if request[0] == "LOGIN":
			if len(request) < 3:
				sendMessage("JAW/1.0 400 ERROR \r\n", connection)
			else:
				#request[2] is a json
				if playerExists(request[1].username):
					sendMessage("JAW/1.0 401 OK \r\n", connection)
				else:
					addPlayer(connection, request[1])
					sendMessage("JAW/1.0 200 OK \r\n", connection)
		# elif request[1] == "PLACE":

		# elif request[1] == "PLAY":

		# elif request[1] == "EXIT":

		# elif request[1] == "WHO":

		else:
			sendMessage("JAW/1.0 400 ERROR \r\n", connection)
		epoll.modify(fileno, select.EPOLLOUT)
		return

server = Server()

if __name__ == '__main__':
	try:
		while True:
			events = epoll.poll(1)
			for fileno, event in events:
				if fileno == serverSocket.fileno():
					# new epoll connection
					connectionSocket, addr = serverSocket.accept()
					connectionSocket.setblocking(0)
					epoll.register(connectionSocket.fileno(), select.EPOLLIN)
					server.addConnection(connectionSocket)
				elif event & select.EPOLLIN:
					#receive client data on epoll connection
					str1 = server.connections[fileno].recv(1024)#.strip()
					if (len(str1) == 0):
						fNum = fileno
						epoll.unregister(fileno)
						server.connections[fNum].close()
						del server.connections[fNum]
					str2 = str1[str1.find(" ") + 1:len(str1)]
					print str2
					#print json.loads(str1[1])
					#server.checkProtocol(fileno)	
				# elif event & select.EPOLLOUT:
				# 	#send server response on epoll connection
				# 	server.connections[fileno].send("HELLO")
				# 	epoll.modify(fileno, 0)
				elif event & select.EPOLLHUP:
					fNum = fileno
					epoll.unregister(fileno)
					server.connections[fNum].close()
					del server.connections[fNum]
	finally:
		epoll.unregister(serverSocket.fileno())
		epoll.close()
		serverSocket.close()
#scp -P 130 server.py jijli@allv25.all.cs.stonybrook.edu:~
#ssh -p 130 jijli@allv25.all.cs.stonybrook.edu
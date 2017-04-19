from argparse import ArgumentParser
from jaw_enums import JAWMethods, JAWResponses, JAWStatuses
import time
import json
import socket


class Player(object):
    def __init__(self, username, server, status=True, gameId=0, timeLoggedIn = None):
        self.username = username  
        self.status = status
        self.gameId = gameId
        self.server = server
        self.lastRequestSent = None
        self.isLoggedIn = False
        if timeLoggedIn != None:
            self.timeLoggedIn = timeLoggedIn          

    def __str__(self):
        print 'username: ', self.username, '\nstatus: ', self.status, '\ngameId: ', self.gameId, '\ntimeLoggedIn: ', self.timeLoggedIn        

    '''main methods'''        
    def login(self):
        '''
        Log the player into the server denoted by server
        '''
        print 'Login in progress ...'
        json_data = json.dumps(self.createPlayerDictionary())        
        message = JAWMethods.LOGIN + " " + json_data + "\r\n\r\n"
        self.lastRequestSent = JAWMethods.LOGIN
        self.sendMessage(message)        

    def play(self, opponent):
        '''
        Send request to server asking to play the specified opponent
        @param opponent the player we wish to versus

        '''
        self.lastRequestSent = JAWMethods.PLAY

    def who(self):
        '''
        Send request to server asking for available users         
        '''
        self.lastRequestSent = JAWMethods.WHO
        return   
        
    def exit(self):
        '''
        Send break up request to server    
        '''
        self.lastRequestSent = JAWMethods.EXIT

    def place(self, move):
        '''
        Send request to server to place move at given location         
        '''
        self.lastRequestSent = JAWMethods.PLACE

    '''Helper methods'''
    def makeRequest(self, request):
        if request == JAWMethods.LOGIN:
            self.login()
        elif:
            print "finish writing rest of code"

    def printBoard(self, board):
        '''
        Display the current game board state
        @param board a list of board indices
        '''
        print "board"     

    def sendMessage(self, message):
        '''
        Send request to client socket with given message
        @param message the message to send to server
        '''
        clientSocket.send(message)
        return

    def createPlayerDictionary(self):
        playerDictionary = {}
        playerDictionary['username'] = self.username
        playerDictionary['status'] = self.status
        playerDictionary['gameId'] = self.gameId
        playerDictionary['timeLoggedIn'] = self.timeLoggedIn
        return playerDictionary    
    
'''utility functions'''
def processResponse(requestState, response):
    '''
    Process the response message returned by the server and take appropriate action
    @param requestState player request state
    @param response response received from the server
    '''
    responseList = self.checkProtocol(response)
    if responseList[0] == JAWResponses.OK and self.requestState == JAWMethods.LOGIN:        
        self.timeLoggedIn = time.time()
        self.isLoggedIn = True
        print "Logged in successfully at time: ", time.strftime("%b %d %Y %H:%M:%S", time.gmtime(self.timeLoggedIn))

def processStdin(stdinInput):
    '''
    Process the stdin input and take appropriate action
    @param stdinInput input received from stdin
    '''
    return

def checkProtocol(packet):
    '''
    Checks to see if response from server is valid protocol
    Raise an exception if it does not
    @return list of extracted protocol details
    '''
    return True   

def checkUsername(username):
    '''Determine whether the username is valid or not'''
    if username.find(" ") == -1:
        return True
    return False

 def help():    
        '''
        Prints the help menu
        '''         
        print "login [username] \t- logs into a server with unique id.  Force quits if username is already taken"
        print "place [index]\t[ 1, 2, 3]"
        print "\t\t [ 4, 5, 6]"
        print "\t\t [ 7, 8, 9]]"
        print "\t\t\t- place your symbol at the corresponding poisition labeled in grid above"
        print "exit\t\t\t- quits the program at any time"
        print "games\t\t\t- obtains a list of all ongoing games along with their respective gameID and players"
        print "who\t\t\t- obtains a list of all players available to play"
        print "play [player] \t\t- challenges the specified player if s/he is available to play"
        print "observe [gameID]\t- tunes into the the specified game"
        print "unobserve [gameID]\t- stops receiving incoming data about particular game"    

if __name__ == "__main__":
    # parse commandline arguments
    usage = "%(prog)s serverName serverPort"
    ap = ArgumentParser(usage = usage)

    # Required Arguments
    ap.add_argument("serverName",
                    help="The name of the machine on which the server is running.")
    ap.add_argument("serverPort",
                    help="The port number that the server is listening at.")
    args = ap.parse_args()
    serverName = args.serverName
    serverPort = int(args.serverPort)

    try:
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #clientSocket.connect((serverName,serverPort))
        while True:
            username = raw_input("Input your username: ")
            if checkUsername(username):
                break
            print "Username must not contain any spaces!"
        player = Player(username, clientSocket)
        player.printInfo()

        # prompt user to log in
        player.login(clientSocket)    
        # dont wait for login response from server, user may wish to exit instead
        # while loop here
        # poll stdin and client socket
        epoll = select.epoll()
        epoll.register(clientSocket.fileno(), select.EPOLLIN)
        

    except socket.error:
        print "Error connecting to server. Exiting ..."
    finally:
        clientSocket.close()



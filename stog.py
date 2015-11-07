import httplib
import json
import urllib
import socket
import getpass



class stogError(Exception):
    def __init__(self, value, critical=False):
	self.value    = value
	self.critical = critical
    def __str__(self):
	return str(self.value)
    def __repr__(self):
	return self.value


class stogClient(object):
    def __init__(self, host = None, port = None, username = None, password = None):
	self.headers = {"Content-type": "application/x-www-form-urlencoded",
			"Accept": "text/json"}
	self.host = host
	self.port = port
	self.username = ''
	self.password = ''
	self.commands = []
	self.srvmsg   = ''
	self.srvauth  = ''

	if host is not None and port is not None:
	    try:
		conn = httplib.HTTPConnection(self.host,self.port)
		conn.request("GET", "/")
		response = conn.getresponse()
		jsr = json.loads(response.read())
		self.commands = jsr['commands']
		self.srvmsg   = jsr['srvmsg']
		self.srvauth  = jsr['srvauth']
	    except socket.error as e:
		raise stogError("[%s:%d] -> %s\n" % (self.host, self.port, e))

	if username is not None and password is not None:
	    self.username = username
	    self.password = password
    
    def getuser(self):
	user = raw_input("Username [%s]: " % getpass.getuser())
	if not user:
    	    self.username = getpass.getuser()
	else:
	    self.username = user
	self.password = getpass.getpass()

    def __command(self, command, arg = None):
	if arg is None:
	    return urllib.urlencode({'username':self.username, 'password':self.password,'command':command})
	else:
	    return utllib.urlencode({'username':self.username, 'password':self.password,'command':command, 'arg':arg})

    def doList(self):
	param = self.__command('LIST')
	try:
	    conn = httplib.HTTPConnection(self.host, self.port)
	    conn.request("POST", "", param, self.headers)
	    response = conn.getresponse()
	    print response.status
	except socket.error as e:
	    raise stogError("[%s:%d] -> %s\n" % (self.host, self.port, e))

	if response.status == 200:
	    jslist = response.read()
	    print jslist

	    

    def doStor(self):
	param = self.__command('STOR')
	pass

    def doRetr(self, filename, WriteCallBack):
	param = self.__command('RETR', filename)
	try: 
	    conn = httplib.HTTPConnection(self.host, self.port)
	    conn.request("POST", "", param, self.headers)
	    response = conn.getresponse()
	except socket.error as e:
	    raise stogError("[%s:%d] -> %s\n" % (self.host, self.port, e))

	if response.status == 200:
	    rsp = json.dumps(response.read())
	    sd  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



def main():
    end  = False
    stog = None
    while not end:
	cmd = raw_input('stog> ')

	if cmd.upper() == 'QUIT':
	    end = True
	elif cmd.upper() == 'CONNECT':
	    host = raw_input('Hostname: ')
	    if host:
		port = raw_input('Port: ')
		if port:
		    stog = stogClient(host,int(port))
		
	elif cmd.upper() == 'LIST':
	    if stog:
		stog.doList()
	    else:
		print "Not connected"
	elif cmd.upper() == 'STOR':
	    pass
	elif cmd.upper() == 'RETR':
	    pass
	else:
	    print "Command not found\n"

if __name__ == "__main__":
    main()







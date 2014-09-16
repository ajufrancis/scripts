#!/usr/bin/env python
#Irongeek's Wacky script for harvesting configs from ASAs
#help from thes sites:
#http://stackoverflow.com/questions/9370886/pexpect-if-else-statement
#http://eli.thegreenplace.net/2010/06/25/aes-encryption-of-files-in-python-with-pycrypto/
#http://linux.byexamples.com/archives/346/python-how-to-access-ssh-with-pexpect/
#and many others
import pexpect, re, getpass, os, time, ConfigParser, base64, hashlib, sys, random, datetime
from Crypto.Cipher import AES
import threading
from threading import Thread
import thread

commandonall="show run"
prefixonall=""

if len(sys.argv)<2:
	sys.exit("I need a config file name to work with. If the file does not exist, we will create it. Use a '-d' after the file name to turn on debugging.")

configpassword = getpass.getpass('Give me the config password or Die!!! : ')
key = hashlib.sha256(configpassword).digest()
keyhash = hashlib.sha256(key).digest()
mode = AES.MODE_CFB
config = ConfigParser.RawConfigParser()
configfilename=sys.argv[1]
#If the file exists, we will read from it
if os.path.exists(configfilename):
	config.read(configfilename)
	#Check if password is correct
	if keyhash != base64.b64decode(config.get('configs', 'Key_Hash')):
		sys.exit ("Wrong Config Password! You Must Die!!!")
	else:
		#If it is correct we can decrypt the INI file
		iv = base64.b64decode(config.get('configs', 'IV'))
		encryptor = AES.new(key, mode, iv)
		hostnamesfile = config.get('configs', 'Host_Names_File')
		asauserpass = encryptor.decrypt(base64.b64decode(config.get('configs', 'ASA_Password')))
		enpass = encryptor.decrypt(base64.b64decode(config.get('configs', 'Enable_Password')))
		asauser = encryptor.decrypt(base64.b64decode(config.get('configs', 'ASA_User')))
else:
	#If it did not exist, we prompt the user to create it
	iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
	encryptor = AES.new(key, mode, iv)
	hostnamesfile = raw_input('Host Names File: ')
	asauser = raw_input('ASA User: ')
	asauserpass = getpass.getpass('ASA User Password: ')
	enpass = getpass.getpass('Enable Password: ')
	config.add_section('configs')
	config.set('configs', 'IV', base64.b64encode(iv))
	config.set('configs', 'Host_Names_File', hostnamesfile)
	config.set('configs', 'Key_Hash', base64.b64encode(keyhash))
	config.set('configs', 'ASA_Password', base64.b64encode(encryptor.encrypt(asauserpass)))
	config.set('configs', 'Enable_Password', base64.b64encode(encryptor.encrypt(enpass)))
	config.set('configs', 'ASA_User', base64.b64encode(encryptor.encrypt(asauser)))
	with open(configfilename, 'wb') as configfile:
		config.write(configfile)


class GrabConfig(Thread):
	def __init__ (self,host):
		Thread.__init__(self)
		self.host = host.replace("\n","").replace("\r","")
		self.status = -1
	def run(self):
		try:
			print "Running on " + self.host
			child = pexpect.spawn ('ssh ' + asauser + '@' + self.host)
			child.maxread=9999999
			if "-d" in sys.argv:
				child.logfile = sys.stdout
			i=child.expect(['.*assword:.*',pexpect.EOF,pexpect.TIMEOUT],1)
			if i==0:
				print "Sending SSH Password to " + self.host,
				child.sendline(asauserpass)
			elif i==1:
				print "Connection to " + self.host + " Dropped"
				thread.exit()
			elif i==2: #timeout
				print "Connection to " + self.host + " Timeout"
				thread.exit()
			child.sendline("\r")
			child.expect('.*>.*')
			child.sendline('en')
			child.expect('.*assword:.*')
			child.sendline(enpass)
			child.expect(".*# ")
			if "/admin" in child.after: # Only need to do this if we have contexts
				child.sendline('changeto system')
				child.expect(".*# ")
			child.sendline("terminal pager 0") #So "show run" keeps going
			child.expect(".*# ")
			child.sendline("\r")
			child.expect(".*# ")
			asaname = child.after.replace("#","").replace("\n","").replace("\r","").replace(" ","")
			child.sendline("show run | grep context")
			child.expect(".*# ")
			#Plan to to replace the below when I have better regex
			contexts = re.findall("^context .*", child.after, re.MULTILINE)
			child.sendline(commandonall) 
			child.expect(".*# ", timeout=200)
			f = open(prefixonall+asaname+"-"+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")+".TXT", 'w')
			configlines=child.after.splitlines()
			f.writelines(["%s\r\n" % line for line in configlines[1:-1]])
			f.close()
			#Loops over each context, and grabs the ASA configs
			for context in contexts:
				context=context[8:].replace("#","").replace("\n","").replace("\r","").replace(" ","")
				print "Working on " + self.host + " in the context " + context + "..."
				child.sendline("ch con "+context)
				child.expect(".*# ")
				child.sendline(commandonall) 
				child.expect(".*# ", timeout=200)
				configlines=child.after.splitlines()
				f = open(prefixonall+asaname +"-"+context+"-"+datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")+".TXT", 'w')
				f.writelines(["%s\r\n" % line for line in configlines[1:-1]])
				f.close()					
			child.sendline('exit')
		except:
			print "Unexpected error:", sys.exc_info()[0]
			print  "Error on "+self.host
			raise
#Main loop of the program that spawns threads to connect to multiple ASAs at the same time 
asalist = open(hostnamesfile).readlines()
for host in asalist:
	GrabConfig(host).start()

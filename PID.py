#!C:\Program Files\Anaconda2\python.exe
from __future__ import print_function
import numpy as np
import time
import argparse
import socket
import sys,re
from pdb import set_trace as br

# Routines to parse command line arguments
parser = argparse.ArgumentParser(description="Log values from encoders")
parser.add_argument('--debug', default=False, action='store_const', const=True, help='Debug Mode/live graphing')
args=parser.parse_args()

# Define an error printing function for error reporting to terminal STD error IO stream
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def udpInit(udp_ip,udp_port):
	global UDP_IP
	global UDP_PORT
	#set ip address
	try:
		assert type(udp_ip)==str
		if not re.match('\\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\\b',udp_ip):
			raise 'n cookie'
		UDP_IP = udp_ip
	except:
		eprint('Error: Provided udp_ip is not a valid ip')
		sys.exit()
	#set port
	try:
		assert type(udp_port)==int and udp_port in xrange(1,49151) #xrange is more memory efficient than range for large ranges
		UDP_PORT = udp_port
	except:
		eprint('Error: Provided port is invalid')
		sys.exit()
	#define socket
	UDP_SOCK = socket.socket(socket.AF_INET, # Internet
							 socket.SOCK_DGRAM) # UDP
	UDP_SOCK.setblocking(0) # make the receive not wait for the buffer to fill before continuing
	udpSend(str('0'),UDP_SOCK) # send simple packet so roboRIO gets the ip address to send to
	return UDP_SOCK
def udpSend(message,sock):
	# try:
	sock.sendto(message, (UDP_IP, UDP_PORT))
	# except socket.error:
		# print('Warning: Could not connect to '+UDP_IP+', port:'+str(UDP_PORT))
	if args.debug:
		print('Sent:'+message)
def udpReceive(sock):
	try:
		data, addr=sock.recvfrom(1024) #buffer size
	except socket.error:
		if args.debug:
			eprint('	Nothing to get from socket: '+UDP_IP+', port:'+str(UDP_PORT))
		return '',''
	if args.debug:
		print(data)
	return data, addr
if __name__ == "__main__":
	sock=udpInit('10.31.40.42',5803)
	udpSend('Hello world',sock)
	f=open('new.txt','a')
	while True:
		received=None
		received,addr=udpReceive(sock)
		if received is not None:
			f.write(received)

#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import Link, Intf, TCLink
from mininet.topo import Topo
from mininet.util import dumpNodeConnections
import logging
import os
import sys
from time import sleep
import random

class SimpleTopo(Topo):

	switchList = []

	host_1 = ""
	host_2 = ""

	length = 0

	def __init__(self, l):

		Topo.__init__(self)
		self.length = int(l)

		for i in xrange(self.length):
			self.switchList.append(self.addSwitch('s'+str(i+1)))

		for i in xrange(self.length-1):
			self.addLink(self.switchList[i], self.switchList[i+1], bw=100, delay='1ms', use_htb=True)

		#self.switch = self.addSwitch('s1')
		self.host_1 = self.addHost('h1', ip='10.0.0.1')
		self.host_2 = self.addHost('h2', ip='10.0.0.2')
		self.addLink(self.host_1, self.switchList[0], bw=10, use_tbf=True)
		self.addLink(self.host_2, self.switchList[self.length-1], bw=100, delay='1ms', use_htb=True)
    	#self.addLink(self.host_1, self.switch, bw=1)
    	#self.addLink(self.host_2, self.switch, bw=1)

def pingTest(net, topo):
	h1 = net.getNodeByName(topo.host_1)
	h2 = net.getNodeByName(topo.host_2)
	net.ping([h1, h2])

def ITGTest(net,topo):
	h1 = net.getNodeByName(topo.host_1)
	h2 = net.getNodeByName(topo.host_2)	
	#print "start h2 as server"
	#h2.cmd('./ITGRecv &')
	#print "start h1 as client"
	#h1.cmd('./ITGSend -l my_sender.log -x my_receiver.log -Sda 10.0.0.2 -t 10000')
	#h1.cmd('./ITGSend -l sender.log -x receiver.log -Sda 10.0.0.2 -t 50000 -o 50 -O 10') 
	#print "client h1 ended"
	sleep(2)
	print "shutdown server h2"
	h2.cmd('killall -9 ITGRecv')


def startExp(length, ip, port, count):
	topo = SimpleTopo(length)
	net = Mininet(topo=topo, link=TCLink, controller=None, autoSetMacs=True, autoStaticArp=True)
	net.addController('controller', controller=RemoteController, ip=ip, port=int(port))
	net.start()

	sleep(3)
	#pingTest(net, topo)
	#sleep(3)
	#ITGTest(net, topo)

	CLI(net)
	net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        startExp(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
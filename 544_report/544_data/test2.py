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
	#vertical_switch_list = []

	host_1 = ""
	host_2 = ""

	host_3 = ""
	host_4 = ""

	length = 0

	def __init__(self, l):

		Topo.__init__(self)

		self.length = int(l)

		if self.length % 2 != 1:
			print "Error: length must be an odd number!"

		for i in xrange(self.length):
			self.switchList.append(self.addSwitch('s'+str(i+1)))

		for i in xrange(self.length-1):
			self.addLink(self.switchList[i], self.switchList[i+1], bw=1, use_tbf=True)

		self.host_1 = self.addHost('h1', ip='10.0.0.1')
		self.host_2 = self.addHost('h2', ip='10.0.0.2')
		self.addLink(self.host_1, self.switchList[0], bw=10, use_tbf=True)
		self.addLink(self.host_2, self.switchList[self.length-1], bw=10, use_tbf=True)

		"""
		# add vertical switches and hosts
		for i in xrange(self.length-1):
			self.vertical_switch_list.append(self.addSwitch('vs'+str(i+1000)))

		for i in xrange(self.length/2-1):
			print "connecting switch %s to %s" %(self.vertical_switch_list[i],self.vertical_switch_list[i+1]) 
			self.addLink(self.vertical_switch_list[i], self.vertical_switch_list[i+1], bw=1, use_tbf=True)
			print "connecting switch %s to %s" %(self.vertical_switch_list[i+self.length/2],self.vertical_switch_list[i+self.length/2+1]) 
			self.addLink(self.vertical_switch_list[i+self.length/2], self.vertical_switch_list[i+self.length/2+1], bw=1, use_tbf=True)

		self.addLink(self.switchList[self.length/2], self.vertical_switch_list[self.length/2-1], bw=10, use_tbf=True)
		self.addLink(self.switchList[self.length/2], self.vertical_switch_list[self.length/2], bw=10, use_tbf=True)
		"""

		self.host_3 = self.addHost('h3', ip='10.0.0.3')
		self.host_4 = self.addHost('h4', ip='10.0.0.4')

		self.addLink(self.host_3, self.switchList[0], bw=10, use_tbf=True)
		self.addLink(self.host_4, self.switchList[self.length-1], bw=10, use_tbf=True)


def pingTest(net, topo):
	h1 = net.getNodeByName(topo.host_1)
	h2 = net.getNodeByName(topo.host_2)
	net.ping([h1, h2])

	h3 = net.getNodeByName(topo.host_3)
	h4 = net.getNodeByName(topo.host_4)
	net.ping([h3, h4])
	#h1.cmdPrint("ping %s -c 3" %(topo.host_2))  

"""
def ITGTest(net,topo):
	h1 = net.getNodeByName(topo.host_1)
	h2 = net.getNodeByName(topo.host_2)	
	print "start h2 as server"
	h2.cmd('./ITGRecv &')
	print "start h1 as client"
	#h1.cmd('./ITGSend -l my_sender.log -x my_receiver.log -Sda 10.0.0.2 -t 10000')
	h1.cmd('./ITGSend -T UDP -a 10.0.0.2 -c 100 -C 1000 -t 150000 -l sender.log -x receiver.log') 
	print "client h1 ended"
	sleep(2)
	print "shutdown server h2"
	h2.cmd('killall -9 ITGRecv')
"""
def iperfTest(net, topo, count):
	h1 = net.getNodeByName(topo.host_1)
	h2 = net.getNodeByName(topo.host_2)
	h3 = net.getNodeByName(topo.host_3)
	h4 = net.getNodeByName(topo.host_4)

	print "start server host 2" 
	h2.cmd("iperf -s -i 1 > server_%s.txt &" %(count))
	print "start server host 4" 
	h4.cmd("iperf -s -i 1 &")
	print "start client host 3"
	h3.cmd("iperf -c 10.0.0.4 -i 1 -t 50 &")
	print "start client host 1"
	h1.cmd("iperf -c 10.0.0.2 -i 1 -t 50")

def startExp(length, ip, port, count):
	topo = SimpleTopo(length)
	net = Mininet(topo=topo, link=TCLink, controller=None, autoSetMacs=True, autoStaticArp=True)
	net.addController('controller', controller=RemoteController, ip=ip, port=int(port))
	net.start()

	sleep(3)
	pingTest(net, topo)
	sleep(3)
	iperfTest(net, topo, count)

	CLI(net)
	net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    if os.getuid() != 0:
        logger.debug("You are NOT root")
    elif os.getuid() == 0:
        startExp(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
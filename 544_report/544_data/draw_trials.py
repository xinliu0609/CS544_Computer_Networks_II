from numpy import arange
import matplotlib.pyplot as plt
import numpy as np
import sys

def plotLine(directory, figureName):
    # first, get iperf data
    iperfResult = []
    for i in xrange(10):
        #print "%d" %(i+1)
        f = open(directory+"server_%s.txt" %(str(i+1)), 'r')
        lines = f.readlines()
        line = lines[-1]
        segments = line.split(' ')
        iperfResult.append(float(segments[-2]))

    headResult = []
    f = open(directory+"Head_switch.txt", 'r')
    lines = f.readlines()
    for line in lines:
        headResult.append(float(line)*8/50000)

    tailResult = []
    f = open(directory+"Tail_switch.txt", 'r')
    lines = f.readlines()
    for line in lines:
        tailResult.append(float(line)*8/50000)

    plt.title('Throughput at Each Trial', fontsize=20)
    plt.ylabel('Throughput (Kbits/sec)', fontsize=18)
    plt.xlabel('Trial Number', fontsize=18)

    row = range(1, len(iperfResult)+1)
    plt.plot(row, iperfResult, linewidth=2)
    plt.plot(row, headResult, linewidth=2)
    plt.plot(row, tailResult, linewidth=2)
    plt.ylim([0, 1000])

    plt.legend(['Iperf', 'Head', 'Tail'])

    plt.savefig(figureName)
    

if __name__ == "__main__":
    plotLine(sys.argv[1], sys.argv[2])
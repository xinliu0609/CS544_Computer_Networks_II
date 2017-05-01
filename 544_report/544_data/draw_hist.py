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

    iperfMean = np.mean(iperfResult)
    iperStd = np.std(iperfResult)
    #print iperfResult
    #print np.mean(iperfResult)
    #print np.std(iperfResult)

    headResult = []
    f = open(directory+"Head_switch.txt", 'r')
    lines = f.readlines()
    for line in lines:
        headResult.append(float(line)*8/50000)

    headMean = np.mean(headResult)
    headStd = np.std(headResult)

    tailResult = []
    f = open(directory+"Tail_switch.txt", 'r')
    lines = f.readlines()
    for line in lines:
        tailResult.append(float(line)*8/50000)

    tailMean = np.mean(tailResult)
    tailStd = np.std(tailResult)

    plt.title('Mean and Standard Deviation of Throughput', fontsize=20)
    plt.ylabel('Throughput (Kbits/sec)', fontsize=18)

    objects = ("Iperf", "Head switch", "Tail switch")
    x = np.arange(len(objects))

    plt.bar(x, [iperfMean, headMean, tailMean], width=0.25, yerr=[iperStd, headStd, tailStd], color='yellow', align='center')
    plt.xticks(x, objects, fontsize=18)
    plt.savefig(figureName)
    

if __name__ == "__main__":
    plotLine(sys.argv[1], sys.argv[2])
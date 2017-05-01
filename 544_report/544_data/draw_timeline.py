from numpy import arange
import matplotlib.pyplot as plt
import numpy
import sys

def getData(filename):
    f = open(filename, 'r')

    result = []

    lines = f.readlines()
    lines = lines[:-1]

    for line in lines:
        segments = line.split(' ')
        if segments[-1] == "Kbits/sec\n":
            result.append(float(segments[-2]))
        elif segments[-1] == "bits/sec\n" :
            result.append(float(segments[-2])/1000000)
        elif segments[-1] == "Mbits/sec\n":
            result.append(1000)
    return result

def plotLine(filename, figureName):
    data = getData(filename)
    row = range(1, len(data)+1)
    print row
    print data

    plt.title('Throughput at Each Second Interval', fontsize=20)
    plt.xlabel('Time (Second)', fontsize=18)
    plt.ylabel('Throughput (Kbits/sec)', fontsize=18)
    plt.plot(row, data)
    #plt.show()
    plt.savefig(figureName)

if __name__ == "__main__":
    """
    for i in range(1, 11): p(i)
    plt.show()
    plotAllversion()
    p(9)
    plt.savefig("./one.png")
    """
    plotLine(sys.argv[1], sys.argv[2])
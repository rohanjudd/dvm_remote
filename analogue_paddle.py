import time
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from dvm import DVM

dvm = DVM()

mode = 1

class AnalogPlot:
    def __init__(self, maxLen):
        dvm.connect()
        self.ax = deque([0.0] * maxLen)
        self.maxLen = maxLen
        self.t = 0

    def addToBuf(self, buf, val):
        if len(buf) < self.maxLen:
            buf.append(val)
        else:
            buf.popleft()
            buf.append(val)

    def update(self, frameNum, a0, text1, text2, pl):
        try:
            val = dvm.read_value()
            if val > 4:
                pl.ylim(4.450, 4.550)
            else:
                pl.ylim(0.470, 0.505)
            diff = int((val - self.ax[-4]) * 10000)
            text1.set_text("v = {0:.4f}".format(val))
            text2.set_text("d = {}".format(diff))
            self.addToBuf(self.ax, val)
            a0.set_data(range(self.maxLen), self.ax)
        except KeyboardInterrupt:
            print('exiting')
        new = self.millis()
        print('millis: {}'.format(new - self.t))
        self.t = new
        return a0,

    # clean up
    def close(self):
        # close serial
        self.ser.flush()
        self.ser.close()

    def millis(self):
        return int(round(time.time() * 1000))


# main() function
def main():
    analogPlot = AnalogPlot(50)

    print('plotting data...')

    # set up animation
    plt.rcParams['toolbar'] = 'None'
    fig = plt.figure(num=None, figsize=(16, 12), dpi=80, facecolor='w', edgecolor='k')
    if mode:
        ax = plt.axes(xlim=(0, 50), ylim=(4.450, 4.550))
    else:
        ax = plt.axes(xlim=(0, 50), ylim=(0.470, 0.505))
    #plt.ylim(0.5,1)
    plt.axhline(y= 0.4750, linewidth=2, color='r')
    plt.axhline(y= 0.4800, linewidth=2, color='b')
    plt.axhline(y= 0.4850, linewidth=2, color='g')
    plt.axhline(y= 0.5000, linewidth=2, color='g')
    plt.axhline(y= 0.4950, linewidth=2, color='r')

    plt.axhline(y= 4.450, linewidth=2, color='r')
    plt.axhline(y= 4.500, linewidth=2, color='g')
    plt.axhline(y= 5.550, linewidth=2, color='r')
    fig.suptitle('Analogue Paddle Output', fontsize=14, fontweight='bold')

    #fig.subplots_adjust(top=0.85)
    ax.set_ylabel('Voltage (V)')
    if mode:
        voltage_label = ax.text(0.5, 0.5, 'v =', verticalalignment='top', horizontalalignment='center', transform=ax.transAxes, color='green', fontsize=20)
        diff_label = ax.text(0.5, 0.5, 'd =', verticalalignment='bottom', horizontalalignment='center', transform=ax.transAxes, color='red', fontsize=20)
    else:
        voltage_label = ax.text(35, 0.473, 'v =', verticalalignment='top', horizontalalignment='center', color='green', fontsize=20)
        diff_label = ax.text(35, 0.472, 'd =', verticalalignment='top', horizontalalignment='center', color='red', fontsize=20)
    a0, = ax.plot([], [])

    anim = animation.FuncAnimation(fig, analogPlot.update, fargs=(a0, voltage_label, diff_label, plt), interval=100)

    plt.show()

    # clean up
    analogPlot.close()

print('exiting.')  # call main
if __name__ == '__main__':
    main()

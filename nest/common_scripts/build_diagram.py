import numpy
import pylab
import os

#TODO change directory
path = "/home/alex/GitHub/NEUCOGAR/nest/dopamine/test_results/test400_8/"
dpi_n = 120


def spike_make_diagram(ts, gids, name, title, hist):
    pylab.figure()
    color_marker = "."
    color_bar = "blue"
    color_edge = "black"
    ylabel = "Neuron ID"

    if hist == "True":
        #TODO this part doesn't work! Trying to fix
        hist_binwidth = 5.0
        ts1 = ts
        neurons = gids

        ax1 = pylab.axes([0.1, 0.3, 0.85, 0.6])
        pylab.plot(ts1, gids, color_marker)
        pylab.ylabel(ylabel)
        pylab.xticks([])
        xlim = pylab.xlim()

        pylab.axes([0.1, 0.1, 0.85, 0.17])
        t_bins = numpy.arange(numpy.amin(ts), numpy.amax(ts), hist_binwidth)
        n, bins = pylab.histogram(ts, bins=t_bins)
        num_neurons = len(numpy.unique(neurons))
        print "num_neurons " + str(num_neurons)
        heights = 1000 * n / (hist_binwidth * num_neurons)
        print "t_bins " + str(len(t_bins)) + "\n" + str(t_bins) + "\n" + \
               "height " + str(len(heights)) + "\n" + str(heights) + "\n"
        #bar(left,height, width=0.8, bottom=None, hold=None, **kwargs):
        pylab.bar(t_bins, heights, width=hist_binwidth, color=color_bar, edgecolor=color_edge)
        pylab.yticks([int(a) for a in numpy.linspace(0.0, int(max(heights) * 1.1) + 5, 4)])
        pylab.ylabel("Rate (Hz)")
        pylab.xlabel("Time (ms)")
        pylab.xlim(xlim)
        pylab.axes(ax1)
    else:
        pylab.plot(ts, gids, color_marker)
        pylab.xlabel("Time (ms)")
        pylab.ylabel(ylabel)

    pylab.title(title)
    pylab.draw()
    pylab.savefig(path + name + ".png", dpi=dpi_n, format='png')
    pylab.close()



def voltage_make_diagram(times, voltages, name, title):
    timeunit="ms"
    line_style = ""
    if not len(times):
        raise nest.NESTError("No events recorded! Make sure that withtime and withgid are set to True.")
    pylab.plot(times, voltages, line_style, label=title)
    pylab.ylabel("Membrane potential (mV)")
    pylab.xlabel("Time (%s)" % timeunit)
    pylab.legend(loc="best")
    pylab.title(title)
    pylab.draw()
    pylab.savefig(path + name + ".png", dpi=dpi_n, format='png')
    pylab.close()



block = [filename for filename in os.listdir(path) if filename[0] == "@"]

listing = []

for filename in block:
    x_vals = []
    y_vals = []

    if filename.startswith('@spikes'):
        with open(path + filename, 'r') as f:
            header = f.readline()
            log = list( v.strip() for k, v in (item.split(':') for item in header.split(',')) )
            for line in f:
                for item in line[line.index("[")+1 : line.index("]")].split(","):
                    x_vals.append(float(line[:6]))
                    y_vals.append(int(item))
        spike_make_diagram(x_vals, y_vals, log[0], log[1], log[2])
    else:
        with open(path + filename, 'r') as f:
            header = f.readline()
            log = list( v.strip() for k, v in (item.split(':') for item in header.split(',')) )
            for line in f:
                x, y = line.split()
                x_vals.append(x)
                y_vals.append(y)
        voltage_make_diagram(x_vals, y_vals, log[0], log[1])

    print filename + " diagram created"

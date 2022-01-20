import matplotlib.pyplot as plotpy
import numpy
import sys

from dhbw import dasp


def exit():

    sys.exit()


def show():

    plotpy.show()
    return dasp.plot


def figure(name=None):

    plotpy.figure(name)
    return dasp.plot


def plot(*args, **kwargs):

    plotpy.plot(*args, **kwargs)

    return plot


def signal(x, y=None, l=None, p=(-1.1, +1.1)):

    if y is not None:
        plotpy.plot(x, y)
    else:
        plotpy.plot(x)

    if l:
        plotpy.xlim(0, l)

    if p:
        plotpy.ylim(p)

    return plot


class filter:

    def frequency(b, a, fs=None, fn=1024):

        fs = fs if fs is not None else dasp.FS

        w, h = dasp.filter.frequency(b, a, fs=fs, fn=fn)

        plotpy.plot(w, dasp.math.abs(h, db=True))
        plotpy.xlabel('Frequency [Hz]')
        plotpy.ylabel('Response [dB]')

        return plotpy

    def poleszeros(b, a):
        """See also: https://gist.github.com/endolith/4625838"""

        p = dasp.filter.poles(b, a)
        z = dasp.filter.zeros(b, a)

        c = plotpy.Circle((0, 0), radius=1, linestyle=':', linewidth=1, color='black', fill=False, alpha=0.3)
        r = numpy.amax(numpy.concatenate((numpy.abs(p), numpy.abs(z), [1]))) + 0.1

        axis = plotpy.gca()

        axis.add_patch(c)
        axis.axvline(0, linestyle=':', linewidth=1, color='black', alpha=0.3)
        axis.axhline(0, linestyle=':', linewidth=1, color='black', alpha=0.3)

        if len(p):
            axis.plot(p.real, p.imag, 'x', markersize=10, color='red', alpha=0.7, label='Pole')

        if len(z):
            axis.plot(z.real, z.imag, 'o', markersize=10, color='none', markeredgecolor='blue', alpha=0.7, label='Zero')

        axis.legend()
        axis.set_xlabel('Re(z)')
        axis.set_ylabel('Im(z)')

        axis.axis('scaled')
        axis.axis([-r, +r, -r, +r])

        return plotpy

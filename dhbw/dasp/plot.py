import matplotlib.pyplot as plotpy
import numpy
import sys

from dhbw import dasp


def exit():

    sys.exit()


def show():

    plotpy.show()
    return dasp.plot


def tight():

    plotpy.tight_layout()
    return dasp.plot


def figure(name=None):

    plotpy.figure(name)
    return dasp.plot


def plot(*args, **kwargs):

    plotpy.plot(*args, **kwargs)

    return dasp.plot


def signal(x, y=None, xlim=None, ylim=1.1):

    def lim():

        if xlim is not None:
            if isinstance(xlim, (list, tuple)):
                plotpy.xlim(xlim)
            else:
                plotpy.xlim(0, xlim)

        if ylim is not None:
            if isinstance(ylim, (list, tuple)):
                plotpy.ylim(ylim)
            else:
                plotpy.ylim(-ylim, +ylim)

    if y is None:

        assert x is not None
        y = x
        x = None

    if isinstance(y, dict):
        for i, (k, v) in enumerate(y.items()):
            plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)
            if x is not None:
                plotpy.plot(x, v)
            else:
                plotpy.plot(v)
            lim()
    elif isinstance(y, (list, tuple)):
        for i, v in enumerate(y):
            plotpy.gcf().add_subplot(len(y), 1, i + 1)
            plotpy.plot(x, v)
            if x is not None:
                plotpy.plot(x, v)
            else:
                plotpy.plot(v)
            lim()
    else:
        if x is not None:
            plotpy.plot(x, y)
        else:
            plotpy.plot(y)
        lim()

    if x is not None:

        plotpy.xlabel('s')

    return dasp.plot


class fft:

    def abs(x, y, xlim=None, ylim=-120, **kwargs):

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(ylim, 0)

        assert x is not None
        assert y is not None

        if isinstance(y, dict):
            for i, (k, v) in enumerate(y.items()):
                plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)
                f, a = dasp.fft.abs(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('dB')
                lim()
        elif isinstance(y, (list, tuple)):
            for i, v in enumerate(y):
                plotpy.gcf().add_subplot(len(y), 1, i + 1)
                plotpy.plot(x, v)
                f, a = dasp.fft.abs(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('dB')
                lim()
        else:
            f, a = dasp.fft.abs(x, y, **kwargs)
            plotpy.plot(f, a)
            plotpy.ylabel('dB')

        plotpy.xlabel('Hz')

        return dasp.plot

    def arg(x, y, xlim=None, ylim=None, **kwargs):

        def lim():

            if xlim is not None:
                if isinstance(xlim, (list, tuple)):
                    plotpy.xlim(xlim)
                else:
                    plotpy.xlim(0, xlim)

            if ylim is not None:
                if isinstance(ylim, (list, tuple)):
                    plotpy.ylim(ylim)
                else:
                    plotpy.ylim(ylim, 0)

        assert x is not None
        assert y is not None

        if isinstance(y, dict):
            for i, (k, v) in enumerate(y.items()):
                plotpy.gcf().add_subplot(len(y), 1, i + 1, title=k)
                f, a = dasp.fft.arg(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('rad')
                lim()
        elif isinstance(y, (list, tuple)):
            for i, v in enumerate(y):
                plotpy.gcf().add_subplot(len(y), 1, i + 1)
                plotpy.plot(x, v)
                f, a = dasp.fft.arg(x, v, **kwargs)
                plotpy.plot(f, a)
                plotpy.ylabel('rad')
                lim()
        else:
            f, a = dasp.fft.arg(x, y, **kwargs)
            plotpy.plot(f, a)
            plotpy.ylabel('rad')

        plotpy.xlabel('Hz')

        return dasp.plot

    def spectrogram(x, y, s, t, xlim=None, ylim=None, clim=-120, **kwargs):

        s, t, f = dasp.fft.stft(x, y, s, t)
        s = dasp.math.abs(s)

        extent = [numpy.min(t), numpy.max(t), numpy.max(f), numpy.min(f)]

        plotpy.imshow(s.T, extent=extent, aspect='auto', cmap='magma', interpolation='nearest')
        cbar = plotpy.colorbar()

        plotpy.xlabel('s')
        plotpy.ylabel('Hz')
        cbar.set_label('dB')

        if xlim is not None:
            if isinstance(xlim, (list, tuple)):
                plotpy.xlim(xlim)
            else:
                plotpy.xlim(0, xlim)

        if ylim is not None:
            if isinstance(ylim, (list, tuple)):
                plotpy.ylim(ylim[::-1])
            else:
                plotpy.ylim(ylim, 0)

        if clim is not None:
            if isinstance(clim, (list, tuple)):
                plotpy.clim(clim)
            else:
                plotpy.clim(clim, 0)

        # revert y axis
        axis = plotpy.gca()
        axis.set_ylim(axis.get_ylim()[::-1])

        return dasp.plot


class filter:

    def frequency(b, a, n=1024, sr=None):

        sr = sr if sr is not None else dasp.SR

        w, h = dasp.filter.frequency(b, a, n=n, sr=sr)

        plotpy.plot(w, dasp.math.abs(h, db=True))
        plotpy.xlabel('Frequency [Hz]')
        plotpy.ylabel('Response [dB]')

        return dasp.plot

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

        return dasp.plot

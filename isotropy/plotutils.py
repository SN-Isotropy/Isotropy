#!/usr/bin/env python

"""
module to help in plotting. 
Functions: 
	inputExplorer: slider functionality to help in exploring functions
	drawxband    : drawing shaded regions of specific width around a value, 
		helpful in ratio/residual plots
	settwopanel  : returns a figure and axes for two subplots to show the
		functional form and differentials of the function with reference
		to a fiducial set of values. 
"""
import typeutils as tu
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Slider, Button

__all__ = ['inputExplorer', 'settwopanel', 'threepanel', 'drawxband']


def inputExplorer(f, sliders_properties, wait_for_validation=False):
    """ A light GUI to manually explore and tune the outputs of a function.
    taken from http://zulko.wordpress.com/2012/08/18/a-gui-for-the-exploration-of-functions-with-python-matplotlib/


    args:
            f : callable function to return values (for text outputs) or 
                    plot figure. For graphics, it should clear an axes ax
                    and plot the function with its parameter values on 
                    the figure.
                    Example: def func(a) :
                                    ax.clear()
                                    ax.plot( x, np.sin(a*x)
                                    fig.canvas.draw()

            slider_properties: list of dicts
                    arguments for Slider: each element of the list should be 			be a dict with keys "label", "valmax", "valmin" with
                    string, float, float values respectively. There should 
                    be a dict corresponding to each variable to vary in the 
                    slider. 
                    Example: [{"label":"a", "valmax" :2.0, "valmin":-2.0}]

            status: 
                    tested , R. Biswas, Tue Apr 29 10:43:07 CDT 2014
            example_usage:
            >>> x = np.arange(0,10,0.1)
            >>> fig, ax = plt.subplots(1)
            >>> def func (a , doclear = True) :
            >>>	if doclear:
            >>>		ax.clear()
            >>> 	ax.plot( x, np.sin(a*x) )
            >>>	fig.canvas.draw()

            >>> inputExplorer ( func, [{'label':'a', 'valmin' : -1, 'valmax' : 1}])


    """
    nVars = len(sliders_properties)
    slider_width = 1.0 / nVars
    print slider_width
    # CREATE THE CANVAS
    figure, ax = plt.subplots(1)
    figure.canvas.set_window_title("Inputs for '%s'" % (f.func_name))
    # choose an appropriate height
    width, height = figure.get_size_inches()
    height = min(0.5 * nVars, 8)
    figure.set_size_inches(width, height, forward=True)
    # hide the axis
    ax.set_frame_on(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    # CREATE THE SLIDERS
    sliders = []
    for i, properties in enumerate(sliders_properties):
        ax = plt.axes([0.1, 0.95 - 0.9 * (i + 1) * slider_width,
                       0.8, 0.8 * slider_width])
        sliders.append(Slider(ax=ax, **properties))
    # CREATE THE CALLBACK FUNCTIONS

    def on_changed(event):
        res = f(*(s.val for s in sliders))
        if res is not None:
            print res

    def on_key_press(event):
        if event.key is 'enter':
            on_changed(event)
    figure.canvas.mpl_connect('key_press_event', on_key_press)
    # AUTOMATIC UPDATE ?
    if not wait_for_validation:
        for s in sliders:
            s.on_changed(on_changed)
    # DISPLAY THE SLIDERS
    plt.show()


def drawxband(refval,
              xlims=None,
              color='gray',
              bandwidths=[-0.1, 0.1],
              ua=None):
    """
    draw a shaded band of color color of certain width around a single 
    reference value refval
    Parameters
    ----------
    refval : float , mandatory
        scalar (single) reference value, 
        Example: refval  = 1.0
    xlims : list of two floats, optional, defaults to None min and max x
        values through which the band will be drawn. if None, these values are
        set from the limits of the supplied axessubplot. If axessubplots is not
        supplied this will raise an error
    color : python color style, optional,defaults to 'gray' color of the band
    bandwidths : list of two floats, optional default to [-0.1, 0.1] width of
        the band to be shaded. 
    ua  : optional, defaults to None
        `~matplotlib.pyplot.axes.subplot` instance on which to, if None,
        obtains the current axes
    returns:
            axes object
    example usage:
            >>> #To use an existing axes subplot object
            >>> drawxband (refval = 60., bandwidths = [-20.,20.], color = 'green', ua = myax0)	
            >>> #No axes object is available
            >>> drawxband (refval = 60., xlims = [4., 8.] , bandwidths = [-20.,20.],color = 'green')	

    status: Tests in plot_utils main. 
            tested R. Biswas, Fri Apr 18 08:29:54 CDT 2014 

    """
    if ua is None:
        ua = plt.gca()
    else:
        # plt.sca(ua)
        xl, xh = ua.get_xlim()
        if xlims is None:
            xlims = [xl, xh]

    # really started this conditional statement to make it general,
    # but have not finished, will always go to the else condition
    # in current implementation
    if xlims is None:
        if not tu.isiterable(refval):
            raise ValueError( "To draw band supply either refval as numpy"
                              "array or xlims over which it should be drawn")

    else:
        xvals = np.linspace(xlims[0], xlims[1], 2)

        # refvals = refval *np.ones(len(xvals)

    # plot reference value
    ua.axhline(refval, color='k', lw=2.0)
    # draw band
    ua.fill_between(xvals, refval + bandwidths[0], refval + bandwidths[1],
                    color=color, alpha=0.25)

    return ua


def settwopanel(height_ratios=[1.0, 0.3],
                width_ratios=[1., 0.],
                padding=None,
                setdifflimits=[0.9, 1.1],
                setoffset=None,
                setgrid=[True, True],
                figsize=None):
    """
    returns a figure and axes for a main panel and a lower panel for 
    showing differential information of overplotted quantities in
    the top panel. 
    args	:
            height_ratios: list of floats, optional defaults to 
                            [1.0, 0.3]
                    height ratio between the upper and lower panel 

            width_ratios :list of floats, optional defaults to 
                            [1.0, 0.0]
                    width ratio between the left and right  panel 

            figsize: figure size  
            setgrid : List of bools, optional, defaults to [True, True] 
                    whether to set grid on the two panels

    returns :
            figure object , ax0 (axes for top panel) , and ax1 
                    (axes for lower panel)

    usage   :
            >>> myfig,  myax0 , myax1 = settwopanel ( )
            >>> myax0.plot( x,  y) 
            >>> myax1.plot(x, x)
            >>> myfig.tight_layout()

    status  :

            tested by 
            R. Biswas, Fri Feb 21 00:52:55 CST 2014
    """
    import matplotlib.ticker as ticker
    majorformatter = ticker.ScalarFormatter(useOffset=False)

    if figsize == None:
        fig = plt.figure()
    else:
        fig = plt.figure(figsize=figsize)

    gs = gridspec.GridSpec(
        2, 1, width_ratios=width_ratios, height_ratios=height_ratios)

    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])

    if setdifflimits != None:
        ax1.set_ylim(setdifflimits)

    ax0.set_xticklabels("", visible=False)
    ax1.yaxis.set_major_formatter(majorformatter)

    if setgrid[0]:

        ax0.grid(True)

    if setgrid[1]:
        ax1.grid(True)

    hpad = 0.0
    #gridspec.update(hpad = hpad)
    return fig, ax0, ax1


if __name__ == "__main__":

    x = np.arange(0, 10, 0.1)
    y = x * x

    fig, ax = plt.subplots(1)

    def func(a, doclear=True):
        if doclear:
            ax.clear()
        ax.plot(x, np.sin(a * x))
        fig.canvas.draw()

    inputExplorer(func, [{'label': 'a', 'valmin': -1, 'valmax': 1}])

    myfig,  myax0, myax1 = settwopanel()

    myax0.plot(x,  y)
    drawxband(refval=60., bandwidths=[-20., 20.], color='green', ua=myax0)
    #myax1.plot(x, x)

    myfig.tight_layout()

    plt.figure()
    plt.plot(x, y)
    drawxband(
        refval=60., xlims=[4., 8.], bandwidths=[-20., 20.], color='green')

    plt.show()


def threepanel():

    fig = plt.figure()
    gs = gridspec.GridSpec(
        3, 1, height_ratios=[0.33, 0.33, 0.33], width_ratios=[1., 0., 0.])
    ax0 = plt.subplot(gs[0])
    ax1 = plt.subplot(gs[1])
    ax2 = plt.subplot(gs[2])

    return gs, fig, ax0, ax1, ax2

from math import floor, log10

import matplotlib.ticker as ticker
import numpy as np
from .get_axis_tick_label import get_axis_tick_label
from .use_sci_notation import use_sci_notation


def find_exp(number) -> int:
    base10 = log10(abs(number))
    return floor(base10)


def blank_at_zero(tick, label):
    tolerance = 1.0e-14
    if type(tick) is np.ndarray:
        index = np.where(abs(tick) < tolerance)
    else:
        temp = np.array(tick)
        index = np.where(abs(temp) < tolerance)
        del temp

    if np.size(index) == 0:
        raise ValueError("Array must span negative to positive values tick=", tick)
    else:
        index = index[0].item()
        label[index] = ""


def get_target_diagram_axes(x, y, option) -> dict:
    """
    Get axes value for target_diagram function.

    Determines the axes information for a target diagram given the axis
    values (X,Y) and the options in the data structure OPTION returned by
    the GET_TARGET_DIAGRAM_OPTIONS function.

    INPUTS:
    x      : values for x-axis
    y      : values for y-axis
    option : dictionary containing option values. (Refer to
             GET_TARGET_DIAGRAM_OPTIONS function for more information.)

    OUTPUTS:
    axes           : dictionary containing axes information for target diagram
    axes['xtick']  : x-values at which to place tick marks
    axes['ytick']  : y-values at which to place tick marks
    axes['xlabel'] : labels for xtick values
    axes['ylabel'] : labels for ytick values
    Also modifies the input variables 'ax' and 'option'

    Author: Peter A. Rochford
        rochford.peter1@gmail.com

    Created on Nov 25, 2016
    Revised on Aug 14, 2022
    """
    # Specify max/min for axes
    foundmax = 1 if option["axismax"] != 0.0 else 0
    if foundmax == 0:
        # Axis limit not specified
        maxx = np.amax(np.absolute(x))
        maxy = np.amax(np.absolute(y))
    else:
        # Axis limit is specified
        maxx = option["axismax"]
        maxy = option["axismax"]

    # Determine default number of tick marks
    xtickvals = ticker.AutoLocator().tick_values(-1.0 * maxx, maxx)
    ytickvals = ticker.AutoLocator().tick_values(-1.0 * maxy, maxy)
    ntest = np.sum(xtickvals > 0)
    if ntest > 0:
        nxticks = np.sum(xtickvals > 0)
        nyticks = np.sum(ytickvals > 0)

        # Save nxticks and nyticks as function attributes for later
        # retrieval in function calls
        get_target_diagram_axes.nxticks = nxticks
        get_target_diagram_axes.nyticks = nyticks
    else:
        # Use function attributes for nxticks and nyticks
        if hasattr(get_target_diagram_axes, "nxticks") and hasattr(
            get_target_diagram_axes, "nxticks"
        ):
            nxticks = get_target_diagram_axes.nxticks
            nyticks = get_target_diagram_axes.nyticks
        else:
            raise ValueError("No saved values for nxticks & nyticks.")

    # Set default tick increment and maximum axis values
    if foundmax == 0:
        maxx = xtickvals[-1]
        maxy = ytickvals[-1]
        option["axismax"] = max(maxx, maxy)

    # Check if equal axes requested
    if option["equalaxes"] == "on":
        if maxx > maxy:
            maxy = maxx
            nyticks = nxticks
        else:
            maxx = maxy
            nxticks = nyticks

    # Convert to integer if whole number
    if type(maxx) is float and maxx.is_integer():
        maxx = int(round(maxx))
    if type(maxx) is float and maxy.is_integer():
        maxy = int(round(maxy))
    minx = -maxx
    miny = -maxy

    # Determine tick values
    if len(option["ticks"]) > 0:
        xtick = option["ticks"]
        ytick = option["ticks"]
    else:
        tincx = maxx / nxticks
        tincy = maxy / nyticks
        xtick = np.arange(minx, maxx + tincx, tincx)
        ytick = np.arange(miny, maxy + tincy, tincy)

    # Assign tick label positions
    if len(option["xticklabelpos"]) == 0:
        option["xticklabelpos"] = xtick
    if len(option["yticklabelpos"]) == 0:
        option["yticklabelpos"] = ytick

    # define x offset
    thexoffset = find_exp(maxx)
    if use_sci_notation(maxx):
        ixsoffset = True
        xsoffset_str = "$\tx\mathdefault{10^{" + str(thexoffset) + "}}\mathdefault{}$"
    else:
        ixsoffset = False
        xsoffset_str = "None"

    theyoffset = find_exp(maxy)
    if use_sci_notation(maxy):
        iysoffset = True
        ysoffset_str = "$\tx\mathdefault{10^{" + str(theyoffset) + "}}\mathdefault{}$"
    else:
        iysoffset = False
        ysoffset_str = "None"

    # Set tick labels using provided tick label positions
    xlabel = []
    ylabel = []

    # Set x tick labels
    for i in range(len(xtick)):
        index = np.where(option["xticklabelpos"] == xtick[i])
        if len(index) > 0:
            thevalue = xtick[i]
            if ixsoffset:
                thevalue = xtick[i] * (10 ** (-1 * thexoffset))
                label = get_axis_tick_label(thevalue)
                xlabel.append(label)
            else:
                label = get_axis_tick_label(xtick[i])
                xlabel.append(label)
        else:
            xlabel.append("")

    # Set tick labels at 0 to blank
    blank_at_zero(xtick, xlabel)

    # Set y tick labels
    for i in range(len(ytick)):
        index = np.where(option["yticklabelpos"] == ytick[i])
        if len(index) > 0:
            thevalue = ytick[i]
            if iysoffset:
                thevalue = ytick[i] * (10 ** (-1 * theyoffset))
                label = get_axis_tick_label(thevalue)
                ylabel.append(label)
            else:
                label = get_axis_tick_label(ytick[i])
                ylabel.append(label)
        else:
            ylabel.append("")

    # Set tick labels at 0 to blank
    blank_at_zero(ytick, ylabel)

    # Store output variables in data structure
    axes = {}
    axes["xtick"] = xtick
    axes["ytick"] = ytick
    axes["xlabel"] = xlabel
    axes["ylabel"] = ylabel
    axes["xoffset"] = xsoffset_str
    axes["yoffset"] = ysoffset_str

    return axes

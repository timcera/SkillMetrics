"""
How to create a Target diagram with multiple sets of data overlaid

An eighth example of how to create a target diagram given one set of
reference observations and two sets of model predictions for the quantity.

This example shows how to display multiple data sets on the same target 
diagram where a different color marker is used for each data set to
identify its source. This is accomplished by overlaying the points from
the second data set onto the target diagram created using the first data 
set. Three data sets are used in this example where one is the reference
and the other two are model predictions. This example also shows how to
specify the legend using a dictionary instead of a list.

It supports the following arguments as options. 

-noshow : No figure is shown if this flag is present
-nosave : No figure is saved if this flag is present

They can be invoked from a command line as, for example, to not show the
plot to allow batch execution: 

$ python target8.py -noshow

The data sets are yearly time series for years 2001-2014, each stored as
a list in a dictionary having a key of the form 'spi_2001', 'spi_2002', etc.
There is a separate dictionary for each of the observation data set and the 
two model predictions. Each dictionary is written to its own pickle file. 
A different file suffix is used depending upon whether the file is created 
using Python 2 (.pkl) or Python 3 (.pkl3) because the pickle package is not 
cross version compatible for pickle files containing dictionaries.

The data in these files are statistics calculated from yearly time series of 
Standard Precipitation Index value over the Mekong basin, a trans-boundary 
river in Southeast Asia that originates in the Tibetan Plateau and runs 
through China's Yunnan Province, Myanmar, Laos, Thailand, Cambodia, and Vietnam. 
The data sources are the ERA5 climate reanalysis dataset from the European 
Centre for Medium-Range Weather Forecasts (ECMWF) and the Tropical Rainfall 
Measuring Mission (TRMM 3B42 v7) satellite data, whilst the observation data is 
the Asian Precipitation - Highly-Resolved Observational Data Integration 
Towards Evaluation (APHRODITE V1801R1) rain-gauge data. All the statistics for 
the yearly time series are calculated using the observations for 2001 as the 
reference.

This data was provide courtesy of Iacopo Ferrario, Resources Scientist, 
HR Wallingford, Flood and Water Resources group, Wallingford Oxfordshire,
United Kingdom

Author: Peter A. Rochford

Created on Feb 27, 2019
Revised on Aug 28, 2022

@author: rochford.peter1@gmail.com
"""

import argparse
import pickle
from sys import version_info

import matplotlib.pyplot as plt
import numpy as np
import skill_metrics as sm
from matplotlib import rcParams


def load_obj(name):
    # Load object from file in pickle format
    if version_info[0] == 2:
        suffix = "pkl"
    else:
        suffix = "pkl3"

    with open(name + "." + suffix, "rb") as f:
        return pickle.load(f)


class Container(object):
    def __init__(self, target_stats1, target_stats2, taylor_stats1, taylor_stats2):
        self.target_stats1 = target_stats1
        self.target_stats2 = target_stats2
        self.taylor_stats1 = taylor_stats1
        self.taylor_stats2 = taylor_stats2


if __name__ == "__main__":

    # Define optional arguments for script
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-noshow",
        dest="no_show",
        action="store_true",
        help="No figure is shown if this flag is present.",
    )
    arg_parser.add_argument(
        "-nosave",
        dest="no_save",
        action="store_true",
        help="No figure is saved if this flag is present.",
    )
    args = arg_parser.parse_args()
    del arg_parser

    # Set the figure properties (optional)
    rcParams["figure.figsize"] = [6.0, 4.8]
    rcParams["lines.linewidth"] = 1  # line width for plots
    rcParams.update({"font.size": 12})  # font size of axes text

    # Close any previously open graphics windows
    plt.close("all")

    # Read target statistics for ERA Interim (stats1) and TRMM (stats2)
    # data with respect to APHRODITE observations for each of years 2001 to
    # 2014 from pickle file
    stats = load_obj("Mekong_Basin_data")  # observations

    # Specify labels for points in a dictionary because only desire labels
    # for each data set.
    label = {"ERA-5": "r", "TRMM": "b"}

    """
    Produce the target diagram for the first dataset
    """
    if True:
        sm.target_diagram(
            stats.target_stats1["bias"],
            stats.target_stats1["crmsd"],
            stats.target_stats1["rmsd"],
            markercolor="r",
            alpha=0.0,
            ticks=np.arange(-2.0, 2.5, 0.5),
            circles=[0.5, 1.0, 2.0],
            circleLineSpec="k--",
            circleLineWidth=1.0,
        )
    else:
        sm.target_diagram(
            stats.target_stats1["bias"],
            stats.target_stats1["crmsd"],
            stats.target_stats1["rmsd"],
            ticks=np.arange(-2.0, 2.5, 0.5),
            target_options_file="target_option_config.csv",
        )

    """
    Overlay the second dataset
    """
    sm.target_diagram(
        stats.target_stats2["bias"],
        stats.target_stats2["crmsd"],
        stats.target_stats2["rmsd"],
        markercolor="b",
        overlay="on",
        markerLabel=label,
        target_options_file="target_option_config.csv",
    )

    # Write plot to file if arguments say so
    None if args.no_save else plt.savefig("target8.png")

    # Show plot if arguments say so
    None if args.no_show else plt.show()
    plt.close()

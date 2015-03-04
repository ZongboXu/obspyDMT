#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------
#   Filename:  plotxml_report.py
#   Purpose:   Plot the report generated by plotxml flag
#   Author:    Kasra Hosseini
#   Email:     hosseini@geophysik.uni-muenchen.de
#   License:   GPLv3
# -------------------------------------------------------------------

# -----------------------------------------------------------------------
# ----------------Import required Modules (Python and Obspy)-------------
# -----------------------------------------------------------------------

# Required Python and Obspy modules will be imported in this part.
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import sys

add_report = sys.argv[1]
report_fio = open(add_report, 'r')
report_fi = report_fio.readlines()

# --------------------------------------------------------------------
# collect information of good stations:
sta_lat_g = []
sta_lon_g = []
per_phase_diff_g = []
max_diff_g = []

# collect information of bad stations:
sta_lat_b = []
sta_lon_b = []
per_phase_diff_b = []
max_diff_b = []
time_wrong_b = []
id_b = []

sta_lat_time_shift = []
sta_lon_time_shift = []
time_shift = []

for i in range(1, len(report_fi)):
    line_report_fi = report_fi[i].split()
    al_corrected = float(line_report_fi[6]) - float(line_report_fi[7])
    if al_corrected != 0.:
        sta_lat_time_shift.append(float(line_report_fi[3]))
        sta_lon_time_shift.append(float(line_report_fi[4]))
        time_shift.append(al_corrected)
    if float(line_report_fi[1]) > 0. and abs(al_corrected) > 1.e-10:
        sta_lat_b.append(float(line_report_fi[3]))
        sta_lon_b.append(float(line_report_fi[4]))
        per_phase_diff_b.append(float(line_report_fi[1]))
        max_diff_b.append(float(line_report_fi[2]))
        id_b.append(line_report_fi[0])
        time_wrong_b.append(al_corrected)
        print report_fi[i].split('\n')[0]
    elif float(line_report_fi[1]) > 0. and \
                    int(float(line_report_fi[6])*1e5) == 0:
        sta_lat_b.append(float(line_report_fi[3]))
        sta_lon_b.append(float(line_report_fi[4]))
        per_phase_diff_b.append(float(line_report_fi[1]))
        max_diff_b.append(float(line_report_fi[2]))
        id_b.append(line_report_fi[0])
        time_wrong_b.append(al_corrected)
        print report_fi[i].split('\n')[0]
    elif float(line_report_fi[1]) > 0. and \
                    int(float(line_report_fi[7])*1e5) == 0:
        sta_lat_b.append(float(line_report_fi[3]))
        sta_lon_b.append(float(line_report_fi[4]))
        per_phase_diff_b.append(float(line_report_fi[1]))
        max_diff_b.append(float(line_report_fi[2]))
        id_b.append(line_report_fi[0])
        time_wrong_b.append(al_corrected)
        print report_fi[i].split('\n')[0]
    else:
        sta_lat_g.append(float(line_report_fi[3]))
        sta_lon_g.append(float(line_report_fi[4]))
        per_phase_diff_g.append(float(line_report_fi[1]))
        max_diff_g.append(float(line_report_fi[2]))

if len(sta_lat_g) > 0:
    # Plot GOOD stations
    plt.figure()
    m = Basemap(projection='robin', lon_0=0, lat_0=0)
    m.fillcontinents()
    parallels = np.arange(-90, 90, 30.)
    m.drawparallels(parallels, labels=[1, 1, 1, 1], fontsize=18)
    meridians = np.arange(-180., 180., 60.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=18)
    m.drawmapboundary()

    x, y = m(sta_lon_g, sta_lat_g)
    m.scatter(x, y, 20, c=np.array(per_phase_diff_g)*0., marker="o",
              edgecolor='none', zorder=10, cmap='gray', vmin=0., vmax=1.)
    plt.title('Good Stations', size=24, weight='bold')
    plt.savefig('compare_plots_good.png')

if len(sta_lat_time_shift) > 0:
    plt.figure()
    m = Basemap(projection='robin', lon_0=0, lat_0=0)
    m.fillcontinents()
    parallels = np.arange(-90, 90, 30.)
    m.drawparallels(parallels, labels=[1, 1, 1, 1], fontsize=18)
    meridians = np.arange(-180., 180., 60.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=18)
    m.drawmapboundary()

    x, y = m(sta_lon_time_shift, sta_lat_time_shift)
    m.scatter(x, y, 100, c=time_shift, marker="o", edgecolor='none',
              zorder=10, cmap='jet',
              vmin=min(time_shift), vmax=max(time_shift))
    cbar = plt.colorbar(orientation='horizontal', shrink=0.9)
    cbar.ax.tick_params(labelsize=18)
    plt.title('Time Shift', size=24, weight='bold')
    plt.savefig('time_shift.png')

if len(sta_lat_b) > 0:
    # Plot BAD stations
    plt.figure()
    m = Basemap(projection='robin', lon_0=0, lat_0=0)
    m.fillcontinents()
    parallels = np.arange(-90, 90, 30.)
    m.drawparallels(parallels, labels=[1, 1, 1, 1], fontsize=18)
    meridians = np.arange(-180., 180., 60.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=18)
    m.drawmapboundary()

    x, y = m(sta_lon_b, sta_lat_b)
    m.scatter(x, y, 100, c=per_phase_diff_b, marker="o", edgecolor='none',
              zorder=10, cmap='jet',
              vmin=min(per_phase_diff_b), vmax=100.)
    cbar = plt.colorbar(orientation='horizontal', shrink=0.9)
    cbar.ax.tick_params(labelsize=18)
    plt.title('Bad Stations (percentage)', size=24, weight='bold')
    plt.savefig('compare_plots_bad.png')

    plt.figure()
    m = Basemap(projection='robin', lon_0=0, lat_0=0)
    m.fillcontinents()
    parallels = np.arange(-90, 90, 30.)
    m.drawparallels(parallels, labels=[1, 1, 1, 1], fontsize=18)
    meridians = np.arange(-180., 180., 60.)
    m.drawmeridians(meridians, labels=[0, 0, 0, 1], fontsize=18)
    m.drawmapboundary()

    x, y = m(sta_lon_b, sta_lat_b)
    m.scatter(x, y, 100, c=time_wrong_b, marker="o", edgecolor='none',
              zorder=10, cmap='jet',
              vmin=min(time_wrong_b), vmax=max(time_wrong_b))
    cbar = plt.colorbar(orientation='horizontal', shrink=0.9)
    cbar.ax.tick_params(labelsize=18)
    plt.title('Bad Stations (time shift)', size=24, weight='bold')
    plt.savefig('compare_plots_bad_time.png')

    plt.figure()
    plt.hist(per_phase_diff_b, bins=1000)
    plt.xlabel('%Difference', size=24, weight='bold')
    plt.ylabel('#channels', size=24, weight='bold')
    plt.xticks(size=18, weight='bold')
    plt.yticks(size=18, weight='bold')
    plt.title('Difference (percentage)', size=24, weight='bold')

    plt.figure()
    plt.hist(max_diff_b, bins=1000)
    plt.xlabel('abs(maximum difference)', size=24, weight='bold')
    plt.ylabel('#channels', size=24, weight='bold')
    plt.xticks(size=18, weight='bold')
    plt.yticks(size=18, weight='bold')
    plt.title('Maximum Difference (abs)', size=24, weight='bold')

plt.show()

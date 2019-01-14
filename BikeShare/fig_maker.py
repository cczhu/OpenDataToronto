"""
Legend generator, based off of "Reference for matplotlib artists" by Bartosz
Telenczuk (https://matplotlib.org/examples/shapes_and_collections/artist_reference.html).
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection

from matplotlib import cm as mpl_cm
from matplotlib import colors as mpl_colors


bwr_cmap = mpl_cm.get_cmap('bwr')


def label(xy, text):
    plt.text(xy[0], 0.7, text, ha="center", fontname='Open Sans',
             verticalalignment='top', size=12, color='#ffffff')


fig, ax = plt.subplots(figsize=(12, 2))

# Centrepoints for images.
grid = list(zip(np.linspace(1., 11., 6),
                1.3 * np.ones(6)))

# Bike stations
circle = mpatches.Circle(grid[0], 0.1,
                         color=mpl_colors.rgb2hex(bwr_cmap(0.)[:3]))
ax.add_patch(circle)
label(grid[0], "Bike stations")

circle = mpatches.Circle(np.array(grid[1]) + np.array([-0.5, 0.]), 0.1,
                         color=mpl_colors.rgb2hex(bwr_cmap(0.)[:3]))
ax.add_patch(circle)
circle = mpatches.Circle(np.array(grid[1]) + np.array([0.0, 0.]), 0.1,
                         color=mpl_colors.rgb2hex(bwr_cmap(0.55)[:3]))
ax.add_patch(circle)
circle = mpatches.Circle(np.array(grid[1]) + np.array([0.5, 0.]), 0.1,
                         color=mpl_colors.rgb2hex(bwr_cmap(1.)[:3]))
ax.add_patch(circle)
label(grid[1], "Blue: more bikes arriving\nRed: more bikes departing")

circle = mpatches.Circle(np.array(grid[2]) + np.array([-0.5, 0.]), 0.1,
                         color=mpl_colors.rgb2hex(bwr_cmap(1.)[:3]))
ax.add_patch(circle)
circle = mpatches.Circle(np.array(grid[2]) + np.array([-0.05, 0.]), 0.15,
                         color=mpl_colors.rgb2hex(bwr_cmap(1.)[:3]))
ax.add_patch(circle)
circle = mpatches.Circle(np.array(grid[2]) + np.array([0.5, 0.]), 0.2,
                         color=mpl_colors.rgb2hex(bwr_cmap(1.)[:3]))
ax.add_patch(circle)
label(grid[2], "Bigger: more\narrivals / departures")

# Trip trajectories
lx, ly = np.array([[-0.3, 0.3], [0., 0.]])
line = mlines.Line2D(lx + grid[3][0], ly + grid[3][1], lw=3., color='#64ce5f')
ax.add_line(line)
label(grid[3], "Bike trips")

lx, ly = np.array([[-0.3, 0.3], [0.2, 0.2]])
line = mlines.Line2D(lx + grid[4][0], ly + grid[4][1], lw=1., color='#64ce5f')
ax.add_line(line)
lx, ly = np.array([[-0.3, 0.3], [0., 0.]])
line = mlines.Line2D(lx + grid[4][0], ly + grid[4][1], lw=3., color='#64ce5f')
ax.add_line(line)
lx, ly = np.array([[-0.3, 0.3], [-0.2, -0.2]])
line = mlines.Line2D(lx + grid[4][0], ly + grid[4][1], lw=5., color='#64ce5f')
ax.add_line(line)
label(grid[4], "Thicker: more riders")

lx, ly = np.array([[-0.3, 0.3], [0.2, 0.2]])
line = mlines.Line2D(lx + grid[5][0], ly + grid[5][1], lw=3., color='#64ce5f')
ax.add_line(line)
lx, ly = np.array([[-0.3, 0.3], [0., 0.]])
line = mlines.Line2D(lx + grid[5][0], ly + grid[5][1], lw=3., color='#ffa144')
ax.add_line(line)
lx, ly = np.array([[-0.3, 0.3], [-0.2, -0.2]])
line = mlines.Line2D(lx + grid[5][0], ly + grid[5][1], lw=3., color='#fff24c')
ax.add_line(line)
label(grid[5], ("Green: member rider\nOrange: casual rider\n"
                "Yellow: both"))

plt.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.xlim([0, 12])
plt.ylim([0, 2])
plt.axis('off')

fig.savefig('webapp/legend.png', dpi=200, facecolor='#434347')

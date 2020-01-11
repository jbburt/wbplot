"""
Save parcellated cortical scalars as an image. Include a colorbar in the plot.

Note: wbplot must be located somewhere in your system PATH environment variable.

"""

from wbplot.wbplot import pscalar
from wbplot import constants
import matplotlib.pyplot as plt
import matplotlib.colors as clrs
from matplotlib import colorbar
import matplotlib.image as mpimg
from os.path import join
import numpy as np

# If you haven't yet looked at the save_pscalar.py example, go through it now.
# This example will simply show you one way to load the image into matplotlib
# so you can add a colorbar.

output_dir = "/Users/jbb/Desktop"  # change this if you want to try it

# First, we'll save an image of the left cortical myelin map.
pscalars_l = np.array(
    [1.55, 1.50, 1.49, 1.50, 1.48, 1.45, 1.43, 1.62, 1.55, 1.38, 1.35, 1.32,
     1.51, 1.70, 1.39, 1.48, 1.39, 1.34, 1.43, 1.40, 1.39, 1.38, 1.48, 1.74,
     1.26, 1.21, 1.29, 1.29, 1.28, 1.34, 1.39, 1.31, 1.39, 1.40, 1.34, 1.47,
     1.29, 1.25, 1.28, 1.42, 1.26, 1.27, 1.29, 1.22, 1.24, 1.31, 1.34, 1.42,
     1.34, 1.36, 1.44, 1.37, 1.54, 1.43, 1.37, 1.32, 1.16, 1.22, 1.13, 1.23,
     1.14, 1.18, 1.22, 1.18, 1.22, 1.39, 1.26, 1.24, 1.16, 1.19, 1.19, 1.20,
     1.30, 1.27, 1.30, 1.24, 1.20, 1.26, 1.35, 1.34, 1.35, 1.28, 1.27, 1.21,
     1.24, 1.22, 1.19, 1.15, 1.22, 1.18, 1.20, 1.26, 1.20, 1.22, 1.39, 1.31,
     1.29, 1.22, 1.32, 1.29, 1.38, 1.37, 1.32, 1.47, 1.34, 1.17, 1.27, 1.20,
     1.11, 1.41, 1.22, 1.11, 1.26, 1.19, 1.24, 1.28, 1.35, 1.35, 1.72, 1.28,
     1.38, 1.14, 1.16, 1.51, 1.31, 1.30, 1.26, 1.24, 1.33, 1.27, 1.08, 1.19,
     1.22, 1.21, 1.22, 1.23, 1.24, 1.30, 1.36, 1.36, 1.35, 1.35, 1.28, 1.34,
     1.34, 1.34, 1.26, 1.23, 1.25, 1.29, 1.26, 1.40, 1.41, 1.38, 1.20, 1.40,
     1.33, 1.37, 1.37, 1.35, 1.31, 1.26, 1.40, 1.20, 1.16, 1.42, 1.21, 1.32,
     1.30, 1.24, 1.24, 1.13, 1.56, 1.62, 1.39, 1.22, 1.26, 1.17, 1.19, 1.12])
x = (pscalars_l - pscalars_l.mean()) / pscalars_l.std()  # standardize
file_out = join(output_dir, "test.png")
pscalar(file_out=file_out, pscalars=x, hemisphere='left',
        vrange=(-2, 2), cmap='magma', transparent=True)
# Note that you'll want transparent=True if you plan to place the colorbar
# inside the bounding box of the image!

# First let's set up our figure
w, h = constants.LANDSCAPE_SIZE
aspect = w / h
fig = plt.figure(figsize=(3, 3/aspect))
ax = fig.add_axes([0.075, 0, 0.85, 0.85])
cax = fig.add_axes([0.44, 0.02, 0.12, 0.07])

# Now we have to load the map into matplotlib. One way to do this is the
# following:
img = mpimg.imread(file_out)
im = ax.imshow(img)
ax.axis('off')

# Now let's add a colorbar and we're done. We'll use -2 and +2 as the limits,
# since that's what we used for vrange when generating the image.
cnorm = clrs.Normalize(vmin=-2, vmax=2)  # only important for tick placing
cmap = plt.get_cmap('magma')
cbar = colorbar.ColorbarBase(
    cax, cmap=cmap, norm=cnorm, orientation='horizontal')
cbar.set_ticks([-2, 2])  # don't need to do this since we're going to hide them
cax.get_xaxis().set_tick_params(length=0, pad=-2)
cbar.set_ticklabels([])
cax.text(-0.025, 0.4, "-2", ha='right', va='center', transform=cax.transAxes,
         fontsize=6)
cax.text(1.025, 0.4, "+2", ha='left', va='center', transform=cax.transAxes,
         fontsize=6)
cbar.outline.set_visible(False)
ax.text(0.5, 1.015, "Human T1w/T2w", transform=ax.transAxes,
        va='bottom', ha='center', fontsize=9)
ax.text(0.5, 0.1, "z-score", transform=ax.transAxes,
        va='bottom', ha='center', fontsize=6)
plt.savefig(join(output_dir, "colorbar_test.png"), dpi=500)
plt.close()
# voila!

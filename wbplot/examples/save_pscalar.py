"""
Save parcellated cortical scalars as an image.

Note: wbplot must be located somewhere in your system PATH environment variable.

"""

from wbplot import pscalar
from os.path import join
import numpy as np

# Create a fake neuroimaging map where the left hemisphere is the parcellated
# myelin map and the right hemisphere is random noise. Note that this package
# by default only currently supports the HCP MMP1.0 parcellation, which consists
# of 180 parcels per hemisphere
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
pscalars_r = np.random.randn(180)*0.1 + pscalars_l.mean()
pscalars_lr = np.concatenate((pscalars_r, pscalars_l))

# The function used to save images is wbplot.wbplot.pscalar(). The first two
# arguments are required; they are the output file and the input scalar array.
# I'll save to my desktop:
root = "/Users/jbb/Desktop"
fout1 = join(root, "test1.png")
# You don't have to include the PNG extension; if you dont, it will be appended.
# You can change `root` to a directory on your local file system if you want to
# try running the commands below.

# The remaining function arguments are optional; the function is called below
# using the arguments' default values:
pscalar(file_out=fout1, pscalars=pscalars_lr, orientation='landscape',
        hemisphere=None, vrange=None, cmap='magma', transparent=False)
# Running this should produce a bilateral cortical image of `pscalars_lr`.

# If passing unilateral data -- ie, an array of length 180 -- specify the
# hemisphere using the hemisphere argument to plot only that hemisphere.
# Otherwise, leave hemisphere=None and the contralateral hemisphere will be
# padded with zeros.
pscalar(
    file_out=join(root, "test2.png"), pscalars=pscalars_l, hemisphere='left')

# The vrange doesnt look great here. Let's try specifying it.
x = np.copy(pscalars_l)
x -= x.mean()
x /= x.std()
pscalar(
    file_out=join(root, "test3.png"), pscalars=x, hemisphere='left',
    vrange=(-2, 2))
# Way better.

# Lastly, let's continue using the left hemispheric cortical myelin map, but
# change the colormap to viridis, change the image orientation to portrait, and
# make the image background (ie, the white pixels) transparent:
pscalar(
    file_out=join(root, "test4.png"), pscalars=x, hemisphere='left',
    vrange=(-2, 2), cmap='viridis', orientation='portrait', transparent=True)

# If you just want to write your data to a neuroimaging file (and open it in
# Workbench yourself), see the docs for
# `wbplot.utils.images.write_parcellated_image`.

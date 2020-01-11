"""
Save dense bilateral cortical scalars as an image.

Note: wbplot must be located somewhere in your system PATH environment variable.

"""

from wbplot import dscalar
from os.path import join
import numpy as np


# Let's create some random noise to use as our fake neuroimaging map. Bilateral
# cortical maps, the only dense maps currently supported, in standard 32k
# resolution consist of 59412 vertices:
dscalars = np.random.randn(59412)
# Note that if you have a neuroimaging file, you can load data from them into
# python using extract_nifti_data() and extract_gifti_data() from the module
# `wbplot.utils.images`.

# The function used to save images is wbplot.wbplot.dscalar(). The first two
# arguments are required; they are the output file and the input scalar array.
# I'll save to my desktop:
root = "/Users/jbb/Desktop"
fout1 = join(root, "test1.png")
# You don't have to include the PNG extension; if you dont, it will be appended.
# You can change `root` to a directory on your local file system if you want to
# try running the commands below.

# The remaining function arguments are optional; the function is called below
# using the arguments' default values:
dscalar(file_out=fout1, dscalars=dscalars, orientation='landscape',
        hemisphere=None, palette='magma', transparent=False,
        palette_params=None)
# Running this should produce a bilateral cortical image of random noise.

# If you only wish to plot one hemisphere, you may use the hemisphere argument.
# Let's plot the right hemisphere only, but this time with portrait orientation:
dscalar(
    file_out=join(root, "test2.png"), dscalars=dscalars, hemisphere='right',
    orientation='portrait')

# Notice that magma -- a sequential color palette -- probably isnt the best
# choice for data with positive and negative values (assuming the zero value is
# meaningful). Let's use a diverging color palette instead:
dscalar(
    file_out=join(root, "test3.png"), dscalars=dscalars, hemisphere='right',
    orientation='portrait', palette='RY-BC-BL')
# Now it's clear which values are positive and which are negative. You may use
# any color palette support by Connectome Workbench. For a list of them, see
# `wbplot.constants` or navigate to
# https://www.humanconnectome.org/software/workbench-command/-cifti-palette
# and scroll down the page.

# Lastly, for maximum control over the image, you can specify additional
# illustration parameters using the `palette_param` argument. All arguments
# at the URL above are supported. As an example, let's display only positive
# values between 1 and 2:
params = dict()
params['disp-zero'] = False
params['disp-neg'] = False
params['pos-user'] = (1, 2)
dscalar(
    file_out=join(root, "test4.png"), dscalars=dscalars, hemisphere='right',
    orientation='portrait', palette='RY-BC-BL', palette_params=params,
    transparent=True)
# Notice that the transparent argument simply makes the background (ie, the
# white pixels) transparent.

# If you just want to write your data to a neuroimaging file (and open it in
# Workbench yourself), see the docs for
# `wbplot.utils.images.write_dense_image`.

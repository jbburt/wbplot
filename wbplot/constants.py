from os.path import join, abspath, dirname

# Paths to required files
PACKAGE_ROOT = dirname(abspath(__file__))
DATA_DIR = join(PACKAGE_ROOT, "data")
DLABEL_FILE = join(DATA_DIR, "ImageParcellated.dlabel.nii")
DSCALAR_FILE = join(DATA_DIR, "ImageDense.dscalar.nii")
DSCALAR_BACKUP = join(DATA_DIR, ".ImageDense.dscalar.nii")
SCENE_FILE = join(DATA_DIR, "Human.scene")

# Available Workbench color palettes
CMAPS = ['ROY-BIG-BL',
         'videen_style',
         'Gray_Interp_Positive',
         'Gray_Interp',
         'PSYCH-FIXED',
         'RBGYR20',
         'RBGYR20P',
         'RYGBR4_positive',
         'RGRBR_mirror90_pos',
         'Orange-Yellow',
         'POS_NEG_ZERO',
         'red-yellow',
         'blue-lightblue',
         'FSL',
         'power_surf',
         'fsl_red',
         'fsl_green',
         'fsl_blue',
         'fsl_yellow',
         'RedWhiteBlue',
         'cool-warm',
         'spectral',
         'RY-BC-BL',
         'magma',
         'JET256',
         'PSYCH',
         'PSYCH-NO-NONE',
         'ROY-BIG',
         'clear_brain',
         'fidl',
         'raich4_clrmid',
         'raich6_clrmid',
         'HSB8_clrmid',
         'POS_NEG']

# (width, height) tuples for each scene. Note that these must be changed if you
# modify the scene file! These values can be obtained by loading the scene file
# in wb_view and selecting File -> Capture Image from the menu bar at the top of
# your screen.
BILATERAL_SIZE = (1263, 835)
LANDSCAPE_SIZE = (1680, 596)
PORTRAIT_SIZE = (753, 835)

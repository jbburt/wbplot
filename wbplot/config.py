from os.path import join
from .constants import DATA_DIR

# DEFAULT_CMAP_WB = 'magma'  # default workbench color palette
# DEFAULT_CMAP_PLT = 'magma'  # default matplotlib colormap
# # note magma is one of the few (if not the only) colormaps supported in both

PARCELLATIONS_DIR = join(DATA_DIR, "HumanCorticalParcellations")

PARCELLATION_FILE = join(
    PARCELLATIONS_DIR, "Q1-Q6_RelatedValidation210.CorticalAreas_dil_"
                       "Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii")

SCENE_FILE = join(DATA_DIR, "Human.scene")

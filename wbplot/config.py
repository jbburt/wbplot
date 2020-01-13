from os.path import join
from .constants import DATA_DIR

# TODO: add descriptions

PARCELLATIONS_DIR = join(DATA_DIR, "HumanCorticalParcellations")

PARCELLATION_FILE = join(
    PARCELLATIONS_DIR, "Q1-Q6_RelatedValidation210.CorticalAreas_dil_"
                       "Final_Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii")

SCENE_FILE = join(DATA_DIR, "Human.scene")
SCENE_ZIP_FILE = join(DATA_DIR, "scene.zip")

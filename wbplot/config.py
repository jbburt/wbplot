from os.path import abspath, dirname, join
from .constants import DATA_DIR

DEFAULT_CMAP = 'RY-BC-BL'  # Red yellow black blue teal

OUTPUT_DIR = dirname(abspath(__file__))

PARCELLATIONS_DIR = join(DATA_DIR, "HumanCorticalParcellations")

SCENE_FILE = join(DATA_DIR, "Human.scene")

IMAGE_FILE = join(DATA_DIR, "Image.dlabel.nii")  # contains illustrated data!!

DLABEL_FILE = join(
    PARCELLATIONS_DIR, "Q1-Q6_RelatedValidation210.CorticalAreas_dil_Final_"
                       "Final_Areas_Group_Colors.32k_fs_LR.dlabel.nii")

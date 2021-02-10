from wbplot.utils import plots, images
from wbplot import config, constants
from os import system
import platform
from os.path import join, exists, split
from zipfile import ZipFile
import tempfile


def pscalar(file_out, pscalars, orientation='landscape',
            hemisphere=None, vrange=None, cmap='magma', transparent=False):
    """
    Save an image of parcellated scalars using Connnectome Workbench.

    Parameters
    ----------
    file_out : str
        absolute path to filename where image is saved. if `filename` has an
        extension, it must be .png, e.g. fout="/Users/jbb/Desktop/test.png"
    pscalars : numpy.ndarray
        parcel scalar values
    orientation : 'portrait' or 'landscape', default 'landscape'
        orientation of the output image. if hemisphere is None (i.e., if data
        are bilateral), this argument is ignored.
    hemisphere : 'left' or 'right' or None, default None
        which hemisphere `pscalars` correspond to. if bilateral, use None
    vrange : tuple or None, default None
        data (min, max) for plotting
    cmap : str, default 'magma'
        MATPLOTLIB colormap to use for plotting
    transparent : bool, default False
        make all white pixels in resultant image transparent

    Returns
    -------
    None

    Raises
    ------
    RuntimeError : scene file was not copied to temp directory

    """

    # Check file extension
    if file_out[-4:] != ".png":  # TODO: improve input handling
        file_out += ".png"

    # Perform checks on inputs
    cmap = plots.check_cmap_plt(cmap)
    orientation = plots.check_orientation(orientation)
    hemisphere = images.check_parcel_hemi(pscalars, hemisphere)
    if hemisphere is not None:
        images.check_pscalars_unilateral(pscalars)
    else:
        images.check_pscalars_bilateral(pscalars)

    # If `pscalars` is unilateral, pad other hemisphere with zeros
    pscalars = images.map_unilateral_to_bilateral(
        pscalars=pscalars, hemisphere=hemisphere)

    # Write `pscalars` to the neuroimaging file which is pre-loaded into the
    # scene file, and update the colors for each parcel using the file metadata
    temp_dir = tempfile.gettempdir()
    temp_cifti = join(temp_dir, split(constants.DLABEL_FILE)[1])
    images.write_parcellated_image(
        data=pscalars, fout=temp_cifti, cmap=cmap, vrange=vrange)

    # This is just to prevent error messages written to console because
    # ImageDense.dscalar.nii doesn't exist in the scene directory
    dscalar_out = join(temp_dir, split(constants.DSCALAR_FILE)[1])
    # if 'windows' in platform.system().lower():
    #     cmd = f'xcopy /I {constants.DSCALAR_FILE} {dscalar_out}'
    # else:
    cmd = "cp {} {}".format(constants.DSCALAR_FILE, dscalar_out)
    system(cmd)

    # Now copy the scene file & HumanCorticalParcellations directory to the
    # temp directory as well
    with ZipFile(config.SCENE_ZIP_FILE, "r") as z:  # unzip to temp dir
        z.extractall(temp_dir)
    scene_file = join(temp_dir, "Human.scene")
    if not exists(scene_file):
        raise RuntimeError(
            "scene file was not successfully copied to {}".format(scene_file))

    # Map the input parameters to the appropriate scene in the scene file
    scene, width, height = plots.map_params_to_scene(
        dtype='pscalars', orientation=orientation, hemisphere=hemisphere)

    # Call Connectome Workbench's command-line utilities to generate an image
    cmd = 'wb_command -show-scene "{}" {} "{}" {} {}'.format(
        scene_file, scene, file_out, width, height)
    # cmd += " >/dev/null 2>&1"
    system(cmd)

    if transparent:  # Make background (defined as white pixels) transparent
        plots.make_transparent(file_out)


def dscalar(file_out, dscalars, orientation='landscape',
            hemisphere=None, palette='magma', transparent=False,
            palette_params=None):

    """
    Save an image of dense scalars using Connnectome Workbench.

    Parameters
    ----------
    file_out : str
        absolute path to filename where image is saved. if `filename` has an
        extension, it must be .png, e.g. fout="/Users/jbb/Desktop/test.png"
    dscalars : numpy.ndarray
        dense scalar values
    orientation : 'portrait' or 'landscape', default 'landscape'
        orientation of the output image. if hemisphere is None (i.e., if data
        are bilateral), this argument is ignored.
    hemisphere : 'left' or 'right' or None, default None
    palette : str, default 'magma'
        name of color palette
    transparent : bool, default False
        make all white pixels in resultant image transparent
    palette_params : dict or None, default None
        additional (key: value) pairs passed to "wb_command -cifti-palette". for
        more info, see
        https://humanconnectome.org/software/workbench-command/-cifti-palette

    Returns
    -------
    None

    Notes
    -----
    Because of the way this package is written, when plotting dscalars you must
    use one of the color palettes supported by Connectome Workbench. For a list
    of available colormaps, see the wbplot.constants module or visit
    https://www.humanconnectome.org/software/workbench-command/-metric-palette.

    Example usage of `palette_params`:
        palette_params = dict()
        palette_params["disp-zero"] = True
        palette_params["inversion"] = "POSITIVE_WITH_NEGATIVE"
    The above, passed to this function, would invert the color palette and
    display zero-valued scalars (when `fout` is opened in wb_view). Note that
    arguments pos-percent, pos-user, neg-percent, & neg-user are currently not
    supported.

    Raises
    ------
    RuntimeError : scene file was not copied to temp directory

    """

    hemisphere = images.check_dense_hemi(hemisphere)
    palette = plots.check_cmap_wb(palette)
    orientation = plots.check_orientation(orientation)
    images.check_dscalars(dscalars)

    # Write `dscalars` to a new neuroimaging file in a temp directory & update
    # color palette
    temp_dir = tempfile.gettempdir()
    temp_cifti = join(temp_dir, split(constants.DSCALAR_FILE)[1])
    images.write_dense_image(
        dscalars=dscalars, fout=temp_cifti, palette=palette,
        palette_params=palette_params)

    # This is just to prevent error messages written to console because
    # ImageParcellated.dlabel.nii doesn't exist in the scene directory
    dlabel_out = join(temp_dir, split(constants.DLABEL_FILE)[1])
    if 'windows' in platform.system().lower():
        cmd = f'xcopy /I {constants.DLABEL_FILE} {dlabel_out}'
    else:
        cmd = "cp {} {}".format(constants.DLABEL_FILE, dlabel_out)
    system(cmd)

    # Now copy the scene file & HumanCorticalParcellations directory to the
    # temp directory as well
    with ZipFile(config.SCENE_ZIP_FILE, "r") as z:  # unzip to temp dir
        z.extractall(temp_dir)
    scene_file = join(temp_dir, "Human.scene")
    if not exists(scene_file):
        raise RuntimeError(
            "scene file was not successfully copied to {}".format(scene_file))

    scene, width, height = plots.map_params_to_scene(
        dtype='dscalars', orientation=orientation, hemisphere=hemisphere)

    cmd = 'wb_command -show-scene "{}" {} "{}" {} {}'.format(
        scene_file, scene, file_out, width, height)
    # cmd += " >/dev/null 2>&1"
    system(cmd)

    if transparent:
        plots.make_transparent(file_out)

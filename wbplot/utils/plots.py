"""Auxiliary functions for Connectome Workbench & Matplotlib plots. """

from .. import constants
from PIL import Image
# from matplotlib import colors, pyplot as plt, colorbar
# from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm


def make_transparent(img_file):
    """
    Make each white pixel in an image transparent.

    Parameters
    ----------
    img_file : str
        absolute path to a PNG image file

    Returns
    -------
    None

    Notes
    -----
    This function overwrites the existing file.

    """
    img = Image.open(img_file)
    img = img.convert("RGBA")
    pixdata = img.load()
    width, height = img.size
    for y in range(height):
        for x in range(width):
            if pixdata[x, y] == (255, 255, 255, 255):  # if white
                pixdata[x, y] = (255, 255, 255, 0)  # set alpha = 0
    img.save(img_file, "PNG")


def check_cmap_plt(cmap):
    """
    Check that a colormap exists in matplotlib.

    Parameters
    ----------
    cmap : str or None
        a valid matplotlib colormap; if None, return default colormap
        defined in wbplot.config

    Returns
    -------
    cmap : str

    Raises
    ------
    ValueError : colormap is not available matplotlib

    """
    try:
        _ = cm.get_cmap(cmap)
    except ValueError as e:
        raise ValueError(e)
    return cmap


def check_cmap_wb(cmap):
    """
    Check that a colormap exists in Workbench.

    Parameters
    ----------
    cmap : str or None
        a valid Workbench color palette; if None, return default colormap
        defined in wbplot.config

    Returns
    -------
    cmap : str

    Raises
    ------
    ValueError : colormap is not available in Connectome Workbench

    """
    if cmap not in constants.CMAPS:
        raise ValueError(
            '"{}" is not a colormap provided by Connectome Workbench.'.format(
                cmap))
    return cmap


def check_vrange(vrange):
    """
    Check vrange argument (used by other functions).


    Parameters
    ----------
    vrange : tuple or iterable
        data (min, max) for plotting; if iterable, must have length 2

    Returns
    -------
    vrange : tuple

    Raises
    ------
    ValueError : vrange is not length-2 iterable obj with vrange[0] > vrange[1]

    """
    if type(vrange) is not tuple:
        if not hasattr(vrange, "__iter__"):
            raise ValueError(
                'if vrange is not a tuple, it must be an iterable object')
        if len(vrange) != 2:
            raise ValueError("vrange must contain only two elements")
    if vrange[0] >= vrange[1]:
        raise ValueError("vrange[0] must be strictly less than vrange[1]")
    return tuple(list(vrange))


def map_params_to_scene(dtype, orientation, hemisphere):
    """
    Manually map arguments to a scene in a scene file (.scene).

    Parameters
    ----------
    dtype : 'pscalars' or 'dscalars'
        corresponding to parcellated or dense scalars
    orientation : 'landscape' or 'portrait'
        the desired image orientation
    hemisphere : 'left' or 'right' or None
        the desired illustrated hemisphere

    Returns
    -------
    scene : int
        scene number, ie the scene in constants.SCENE_FILE to use
    width : int
        the width of the output image, in pixels
    height : int
        the height of the output image, in pixels

    Raises
    ------
    ValueError : invalid input argument provided

    """
    if dtype == 'pscalars' and hemisphere is None:
        scene = 1
        width, height = constants.BILATERAL_SIZE

    elif (dtype == 'pscalars' and orientation == 'landscape'
          and hemisphere == 'left'):
        scene = 2
        width, height = constants.LANDSCAPE_SIZE

    elif (dtype == 'pscalars' and orientation == 'landscape'
          and hemisphere == 'right'):
        scene = 3
        width, height = constants.LANDSCAPE_SIZE

    elif (dtype == 'pscalars' and orientation == 'portrait'
          and hemisphere == 'right'):
        scene = 4
        width, height = constants.PORTRAIT_SIZE

    elif (dtype == 'pscalars' and orientation == 'portrait'
          and hemisphere == 'left'):
        scene = 5
        width, height = constants.PORTRAIT_SIZE

    elif dtype == 'dscalars' and hemisphere is None:
        scene = 6
        width, height = constants.BILATERAL_SIZE

    elif (dtype == 'dscalars' and orientation == 'landscape'
          and hemisphere == 'left'):
        scene = 7
        width, height = constants.LANDSCAPE_SIZE

    elif (dtype == 'dscalars' and orientation == 'landscape'
          and hemisphere == 'right'):
        scene = 8
        width, height = constants.LANDSCAPE_SIZE

    elif (dtype == 'dscalars' and orientation == 'portrait'
          and hemisphere == 'left'):
        scene = 9
        width, height = constants.PORTRAIT_SIZE

    elif (dtype == 'dscalars' and orientation == 'portrait'
          and hemisphere == 'right'):
        scene = 10
        width, height = constants.PORTRAIT_SIZE

    else:
        raise ValueError("one or more input arguments is invalid")
    return scene, width, height


def check_orientation(orientation):
    """
    Check the orientation argument (used by other package functions).

    Parameters
    ----------
    orientation : 'portrait' or 'landscape'
        the desired orientation of the output image

    Returns
    -------
    str

    Raises
    ------
    ValueError : invalid orientation argument provided

    """
    if orientation not in ['landscape', 'portrait', 'l', 'p']:
        raise ValueError("orientation must be landscape or portrait")
    if orientation == 'l':
        return 'landscape'
    elif orientation == 'p':
        return 'portrait'
    return orientation

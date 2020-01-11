"""Auxiliary functions for Connectome Workbench & Matplotlib plots. """

from .. import constants
from PIL import Image
from matplotlib import colors, pyplot as plt, colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
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

    """
    if cmap not in constants.CMAPS:
        raise RuntimeError(
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

    """
    if type(vrange) is not tuple:
        if not hasattr(vrange, "__iter__"):
            raise RuntimeError(
                'if vrange is not a tuple, it must be an iterable object')
        if len(vrange) != 2:
            raise RuntimeError("vrange must contain only two elements")
    if vrange[0] >= vrange[1]:
        raise RuntimeError("vrange[0] must be strictly less than vrange[1]")
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
        raise RuntimeError(
            "check that your orientation and hemisphere arguments are valid")
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

    """
    if orientation not in ['landscape', 'portrait', 'l', 'p']:
        raise RuntimeError("orientation must be landscape or portrait")
    if orientation == 'l':
        return 'landscape'
    elif orientation == 'p':
        return 'portrait'
    return orientation


# TODO: remove this once you're sure you don't want to keep it
# def wb_cbar(cax, vrange, cmap, orientation='horizontal'):
#     """
#
#     Parameters
#     ----------
#     cax
#     vrange
#     cmap
#     orientation : 'horizontal' or 'vertical'
#         the orientation of the colorbar
#
#     Returns
#     -------
#     cbar : :class:~`colorbar.ColorbarBase` instance
#     """
#     cmap = check_cmap_plt(cmap)
#     cnorm = colors.Normalize(vmin=vrange[0], vmax=vrange[1])
#     cmap = plt.get_cmap(cmap)
#     cbar = colorbar.ColorbarBase(
#         cax, cmap=cmap, norm=cnorm, orientation=orientation)
#     return cbar


# def add_cmap(im, ax, ticks=None, top=True, pad=0.05, size=10, extend=None,
#              lw=None):
#     """
#
#
#     Parameters
#     ----------
#     im
#     ax
#     ticks
#     top
#     pad
#     size
#     extend
#     lw
#
#     Returns
#     -------
#
#     """
#     divider = make_axes_locatable(ax)
#     if top:
#         cax = divider.append_axes("top", size="{}%%".format(size), pad=pad)
#         if extend is not None:
#             cbar = plt.colorbar(
#                 im, cax=cax, orientation='horizontal', extend=extend)
#         else:
#             cbar = plt.colorbar(im, cax=cax, orientation='horizontal')
#         cbar.ax.xaxis.set_ticks_position('top')
#         cbar.ax.xaxis.set_label_position('top')
#     else:
#         cax = divider.append_axes("right", size="{}%%".format(size), pad=pad)
#         if extend is not None:
#             cbar = plt.colorbar(
#                 im, cax=cax, orientation='vertical', extend=extend)
#         else:
#             cbar = plt.colorbar(im, cax=cax, orientation='vertical')
#     if ticks is not None:
#         cbar.set_ticks(ticks)
#     if lw is None:
#         cbar.outline.set_visible(False)
#     elif lw > 0:
#         cbar.outline.set_linewidth(lw)
#     return cax

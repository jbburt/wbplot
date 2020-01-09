from PIL import Image
from .. import config, constants


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


def check_cmap(cmap):
    """

    Parameters
    ----------
    cmap : str or None
        a valid Connectome Workbench colormap; if None, return default colormap
        defined in wbplot.config

    Returns
    -------
    cmap : str

    """
    if cmap is None:
        cmap = config.DEFAULT_CMAP
    elif cmap not in constants.CMAPS:
        raise RuntimeError(
            '"{}" is not a colormap provided by Connectome Workbench.'.format(
                cmap))
    return cmap


def check_pscalars(pscalars):
    """

    Parameters
    ----------
    pscalars : array_like
        parcellated scalars

    Returns
    -------
    None

    """
    if not hasattr(pscalars, '__iter__'):
        raise RuntimeError("pscalars must be an iterable object")
    if not (len(pscalars) == 180 or len(pscalars) == 360):
        raise RuntimeError("pscalars must be length 180 (if unilateral) "
                           "or length 360 (if bilateral)")

"""Auxiliary functions pertaining to the manipulation of neuroimaging files. """

import numpy as np
import nibabel as nib
from .. import constants, config
from . import plots
from os import system, remove
from matplotlib import colors as clrs
from matplotlib import cm
import xml.etree.cElementTree as eT
from nibabel.cifti2.parse_cifti2 import Cifti2Parser


def map_unilateral_to_bilateral(pscalars, hemisphere):
    """
    Map 180 unilateral pscalars to 360 bilateral pscalars, padding contralateral
    hemisphere with zeros.

    Parameters
    ----------
    pscalars : numpy.ndarray
        unilateral parcellated scalars
    hemisphere : 'left' or 'right' or None

    Returns
    -------
    numpy.ndarray

    """
    hemisphere = check_parcel_hemi(pscalars=pscalars, hemisphere=hemisphere)
    if hemisphere is None:
        return pscalars
    pscalars_lr = np.zeros(360)
    if hemisphere == 'right':
        pscalars_lr[:180] = pscalars
    elif hemisphere == 'left':
        pscalars_lr[180:] = pscalars
    return pscalars_lr


def check_pscalars_unilateral(pscalars):
    """
    Check that unilateral pscalars have the expected size and shape.

    Parameters
    ----------
    pscalars : numpy.ndarray
        parcellated scalars

    Returns
    -------
    None

    Raises
    ------
    TypeError : pscalars is not array_like
    ValueError : pscalars is not one-dimensional and length 180

    """
    if not isinstance(pscalars, np.ndarray):
        raise TypeError(
            "pscalars: expected array_like, got {}".format(type(pscalars)))
    if pscalars.ndim != 1 or pscalars.size != 180:
        e = "pscalars must be one-dimensional and length 180"
        e += "\npscalars.shape: {}".format(pscalars.shape)
        raise ValueError(e)


def check_pscalars_bilateral(pscalars):
    """
    Check that bilateral pscalars have the expected size and shape.

    Parameters
    ----------
    pscalars : numpy.ndarray
        parcellated scalars

    Raises
    ------
    TypeError : pscalars is not array_like
    ValueError : pscalars is not one-dimensional and length 360

    """
    if not isinstance(pscalars, np.ndarray):
        raise TypeError(
            "pscalars: expected array_like, got {}".format(type(pscalars)))
    if pscalars.ndim != 1 or pscalars.size != 360:
        e = "pscalars must be one-dimensional and length 180"
        e += "\npscalars.shape: {}".format(pscalars.shape)
        raise ValueError(e)


def check_dscalars(dscalars):
    """
    Check that dscalars have the expected size and shape.


    Parameters
    ----------
    dscalars : numpy.ndarray
        dense scalars

    Returns
    -------
    None

    Raises
    ------
    TypeError : pscalars is not array_like
    ValueError : pscalars is not one-dimensional and length 59412

    """
    if not isinstance(dscalars, np.ndarray):
        raise TypeError(
            "dscalars: expected array_like, got {}".format(type(dscalars)))
    if dscalars.ndim != 1 or dscalars.size != 59412:
        e = "dscalars must be one-dimensional and length 59412"
        e += "\ndscalars.shape: {}".format(dscalars.shape)
        raise ValueError(e)


def check_parcel_hemi(pscalars, hemisphere):
    """
    Check hemisphere argument for package compatibility.

    Parameters
    ----------
    pscalars : numpy.ndarray
        parcels' scalar quantities
    hemisphere : 'left' or 'right' or None
        if bilateral, use None

    Returns
    -------
    'left' or 'right' or None

    Raises
    ------
    RuntimeError : pscalars is not length-360 but hemisphere not indicated
    ValueError : invalid hemisphere argument

    """
    if pscalars.size != 360 and hemisphere is None:
        raise RuntimeError(
            "you must indicate which hemisphere these pscalars correspond to")
    options = ['left', 'l', 'L', 'right', 'r', 'R', None, 'lr', 'LR']
    if hemisphere not in options:
        raise ValueError("{} is not a valid hemisphere".format(hemisphere))
    if hemisphere in ['left', 'l', 'L']:
        return 'left'
    if hemisphere in ['right', 'r', 'R']:
        return 'right'
    if hemisphere in ['None', 'lr', 'LR']:
        return None


def check_dense_hemi(hemisphere):
    """
    Check hemisphere argument for compatibility.

    Parameters
    ----------
    hemisphere : 'left' or 'right' or None
        if bilateral, use None

    Returns
    -------
    'left' or 'right' or None

    Raises
    ------
    ValueError : invalid hemisphere argument

    """
    options = ['left', 'l', 'L', 'right', 'r', 'R', None, 'lr', 'LR']
    if hemisphere not in options:
        raise ValueError("{} is not a valid hemisphere".format(hemisphere))
    if hemisphere in ['left', 'l', 'L']:
        return 'left'
    if hemisphere in ['right', 'r', 'R']:
        return 'right'
    if hemisphere in ['None', 'lr', 'LR']:
        return None


def extract_nifti_data(of):
    """Extract array of scalar quantities from a NIFTI2 image.

    Parameters
    ----------
    of : :class:~`nibabel.Nifti2Image` instance
        the NIFTI2 image from which to extract scalar data

    Returns
    -------
    data : numpy.ndarray

    """
    return np.asanyarray(of.dataobj).squeeze()


def extract_gifti_data(of):
    """Extract array of scalar quantities from a GIFTI image.

    Parameters
    ----------
    of : :class:~`nibabel.gifti.GiftiImage` instance
        the GIFTI image from which to extract scalar data

    Returns
    -------
    data : numpy.ndarray

    """
    return np.asanyarray(of.darrays[0].data).squeeze()


def write_parcellated_image(
        data, fout, hemisphere=None, cmap='magma', vrange=None):
    """
    Change the colors for parcels in a dlabel file to illustrate pscalar data.

    Parameters
    ----------
    data : numpy.ndarray
        scalar map values
    fout : str
        absolute path to output neuroimaging file with *.dlabel.nii* extension
        (if an extension is provided)
    hemisphere : 'left' or 'right' or None, default None
        which hemisphere `pscalars` correspond to. for bilateral data use None
    cmap : str
        a valid MATPLOTLIB colormap used to plot the data
    vrange : tuple
        data (min, max) for plotting; if None, use (min(data), max(data))

    Returns
    -------
    None

    Notes
    -----
    The file defined by wbplot.config.PARCELLATION_FILE is used as a template to
    achieve this. Thus the data provided to this function must be in the same
    parcellation as that file. By default, this is the HCP MMP1.0 parcellation;
    thus, `data` must be ordered as (R_1, R_2, ..., R_180, L_1, L_2, ..., L_180)
    if bilateral. If unilateral, they must be ordered from area V1 (parcel 1) to
    area p24 (parcel 180).
    """

    # Check provided inputs and pad contralateral hemisphere with 0 if necessary
    check_parcel_hemi(pscalars=data, hemisphere=hemisphere)
    cmap = plots.check_cmap_plt(cmap)
    pscalars_lr = map_unilateral_to_bilateral(
        pscalars=data, hemisphere=hemisphere)

    # Change the colors assigned to each parcel and save to `fout`
    c = Cifti()
    c.set_cmap(data=pscalars_lr, cmap=cmap, vrange=vrange)
    c.save(fout)


def write_dense_image(dscalars, fout, palette='magma', palette_params=None):
    """
    Create a new DSCALAR neuroimaging file.

    Parameters
    ----------
    dscalars : numpy.ndarray
        dense (i.e., whole-brain vertex/voxel-wise) scalar array of length 91282
    fout : str
        absolute path to output neuroimaging file with *.dscalar.nii* extension
        (if an extension is provided)
    palette : str, default 'magma'
        name of color palette
    palette_params : dict or None, default None
        additional (key: value) pairs passed to "wb_command -cifti-palette". for
        more info, see
        https://humanconnectome.org/software/workbench-command/-cifti-palette

    Returns
    -------
    None

    Notes
    -----
    For a list of available color palettes, see the wbplot.constants module or
    visit:
    https://www.humanconnectome.org/software/workbench-command/-metric-palette.

    The file defined by wbplot.config.DSCALAR_FILE is used as a template to
    achieve this. Thus the `dscalars` array provided to this function must be
    contain 59412 elements (i.e., it must include both cortical hemispheres).
    Note the subcortex is not currently supported. In standard bilateral
    cortical dscalar files, elements [0,29695] correspond to the left
    hemisphere and elements [29696,59411] correspond to the right hemisphere.
    Thus, you can simply pad the other elements with NaN if you want only a
    single hemisphere to be plotted.

    Example usage of `palette_params`:
        palette_params = dict()
        palette_params["disp-zero"] = True
        palette_params["disp-positive"] = True
        palette_params["disp-negative"] = False
        palette_params["inversion"] = "POSITIVE_WITH_NEGATIVE"
    The above, passed to this function, would invert the color palette and
    display only positive- and zero-valued scalars (when `fout` is opened in
    wb_view).

    Note that if you wish to define vmin and vmax by hand, you should do one of
    the following:

    >> palette_params = {
        "pos-user": (pos_min, pos_max), "neg-user": (neg_min, neg_max)}
    where pos_min is the minimum positive value shown, pos_max is the maximum
    positive value shown, neg_min is the minimum negative (ie, most negative)
    value shown, and neg_max is the maximum negative (ie, least negative) value
    shown

    or

    >> palette_params = {
        "pos-percent": (pos_min, pos_max), "neg-percent": (neg_min, neg_max)}
    where pos_min, pos_max, neg_min, and neg_max are the same as before but
    expressed as *percentages* of the positive and negative values

    Raises
    ------
    ValueError : palette_params contains an invalid key,value pair

    """
    # TODO: add function for users to map from 32k unilateral to CIFTI subset
    # TODO: implement subcortex

    if fout[-12:] != ".dscalar.nii":  # TODO: improve input handling
        fout += ".dscalar.nii"

    new_data = np.copy(dscalars)

    # Load template dscalar file
    of = nib.load(constants.DSCALAR_FILE)
    temp_data = np.asanyarray(of.dataobj)

    # Write new data to file
    data_to_write = new_data.reshape(np.shape(temp_data))
    new_img = nib.Cifti2Image(
        dataobj=data_to_write, header=of.header, nifti_header=of.nifti_header)
    prefix = fout.split(".")[0]
    cifti_palette_input = prefix + "_temp.dscalar.nii"
    nib.save(new_img, cifti_palette_input)

    # Use Workbench's command line utilities to change color palette
    mode = "MODE_AUTO_SCALE"  # default mode (not DMN, haha)
    disp_zero = disp_neg = disp_pos = True
    if palette_params:
        args = list(palette_params.keys())
        if "pos-percent" in args and "neg-percent" in args:
            mode = "MODE_AUTO_SCALE_PERCENTAGE"
        elif "pos-user" in args and "neg-user" in args:
            mode = "MODE_USER_SCALE"
        if "disp-pos" in args:
            disp_pos = palette_params["disp-pos"]
        if "disp-neg" in args:
            disp_neg = palette_params["disp-neg"]
        if "disp-zero" in args:
            disp_zero = palette_params["disp-zero"]
    cmd = "wb_command -cifti-palette {} {} {}".format(
        cifti_palette_input, mode, fout)
    cmd += " -palette-name {}".format(palette)
    cmd += " -disp-zero {}".format(disp_zero)
    cmd += " -disp-pos {}".format(disp_pos)
    cmd += " -disp-neg {}".format(disp_neg)

    # Update command with provided parameters. NOTE these must be consistent
    # with the format expected by "wb_command -cifti-palette": see
    # https://www.humanconnectome.org/software/workbench-command/-cifti-palette
    if palette_params:
        for k, v in palette_params.items():
            if k in ["disp-zero", "disp-pos", "disp-neg"]:
                continue
            if hasattr(v, '__iter__'):
                if len(v) != 2:
                    raise ValueError(
                        "palette params must be a dict with values which are "
                        "either strings, numbers, or tuples")
                cmd += " -{} {} {}".format(k, v[0], v[1])
            else:
                cmd += " -{} {}".format(k, v)

    # We're ready to change palette and save new file to `fout`
    system(cmd)

    # Remove file which was only used temporarily
    remove(cifti_palette_input)


class Cifti(object):
    """
    A class for changing the colors inside the metadata of a DLABEL neuroimaging
    file. Some of this code was contributed by Dr. Murat Demirtas while he was
    a post-doctoral researcher at Yale.
    """

    def __init__(self):
        of = nib.load(config.PARCELLATION_FILE)  # must be a DLABEL file!!
        self.data = np.asanyarray(of.dataobj)
        self.header = of.header
        self.nifti_header = of.nifti_header
        self.extensions = eT.fromstring(
            self.nifti_header.extensions[0].get_content().to_xml())
        self.vrange = None
        self.ischanged = False

    def set_cmap(self, data, cmap='magma', vrange=None, mappable=None):
        """
        Map scalar data to RGBA values and update file header metadata.

        Parameters
        ----------
        data : numpy.ndarray
            scalar data
        cmap : str or None, default 'magma'
            colormap to use for plotting
        vrange : tuple or None, default None
            data (min, max) for illustration; if None, use (min(data),max(data))
        mappable : Callable[float] or None, default None
            can be used to override arguments `cmap` and `vrange`, e.g. by
            specifying your own map from scalar input to RGBA output

        Returns
        -------
        None

        """
        if data.size != 360:
            raise RuntimeError(
                "pscalars must be length 360 for :class:~wbplot.images.Cifti")

        # Check input arguments
        cmap = plots.check_cmap_plt(cmap)
        self.vrange = (
            np.min(data), np.max(data)) if vrange is None else vrange
        self.vrange = plots.check_vrange(self.vrange)

        # Map scalar data to colors (R, G, B, Alpha)
        if mappable is None:
            cnorm = clrs.Normalize(vmin=self.vrange[0], vmax=self.vrange[1])
            clr_map = cm.ScalarMappable(cmap=cmap, norm=cnorm)
            colors = clr_map.to_rgba(data)
        else:
            colors = np.array([mappable(d) for d in data])

        # Update file header metadata
        for ii in range(1, len(self.extensions[0][1][0][0])):
            self.extensions[0][1][0][0][ii].set(
                'Red', str(colors[ii - 1, 0]))
            self.extensions[0][1][0][0][ii].set(
                'Green', str(colors[ii - 1, 1]))
            self.extensions[0][1][0][0][ii].set(
                'Blue', str(colors[ii - 1, 2]))
            self.extensions[0][1][0][0][ii].set(
                'Alpha', str(colors[ii - 1, 3]))
        self.ischanged = True

    # Write to class attribute self.header
    def write_extensions(self):
        cp = Cifti2Parser()
        cp.parse(string=eT.tostring(self.extensions))
        self.nifti_header.extensions[0]._content = cp.header
        # NOTE if _content is changed to content, this method will break

    def save(self, fout):
        """
        Write self.data to image `fout`.

        Parameters
        ----------
        fout : str
            absolute path to output neuroimaging file. must be a DLABEL file!!

        Returns
        -------
        None

        """
        if self.ischanged:
            self.write_extensions()
        if fout[-11:] != ".dlabel.nii":  # TODO: improve input handling
            fout += ".dlabel.nii"
        new_img = nib.Cifti2Image(
            self.data, header=self.header, nifti_header=self.nifti_header)
        nib.save(new_img, fout)


# Pythonic version of this workbench command (primarily so I don't forget)
def cifti_parcellate(cifti_in, dlabel_in, cifti_out, direction='COLUMN'):
    cmd = "wb_command -cifti-parcellate {} {} {} {}".format(
        cifti_in, dlabel_in, direction, cifti_out)
    system(cmd)

import numpy as np
import nibabel as nib
from .. import constants, config
from . import plots
from os.path import sep, join
import xml.etree.cElementTree as eT
from matplotlib import colors as clrs
from matplotlib import cm


def map_left_to_lr(pscalars_left):
    """
    Map left hemispheric parcel scalars onto bilateral parcel indices.

    Parameters
    ----------
    pscalars_left : array_like

    Returns
    -------
    pscalars_lr : numpy.ndarray

    """

    plots.check_pscalars(pscalars)
    c = nib.load(parcel_labels_lr).get_data()
    dlabels = np.array(c.squeeze(), dtype=int)
    unique_parcels_lr = np.unique(dlabels)
    unique_parcels_left = np.unique(
        nib.load(parcel_labels_l).darrays[0].data)[1:]
    label_to_index_lr = {plbl: i for i, plbl in enumerate(unique_parcels_lr)}
    label_to_index_l = {plbl: i for i, plbl in enumerate(unique_parcels_left)}
    pscalars_lr = np.repeat(pscalars_left.mean(), unique_parcels_lr.size)
    for lbl, idx in label_to_index_l.items():
        scalar_value = pscalars_left[idx]
        pscalars_lr[label_to_index_lr[lbl]] = scalar_value
    return pscalars_lr


def write_parcellated_image(pscalars, fout, vrange=None, cmap=None):
    """
    Insert parcellated scalars into a dlabel file.

    Parameters
    ----------
    pscalars : array_like
    fout
    vrange
    cmap

    Returns
    -------
    None

    Notes
    -----
    This function assumes that the ordering of parcels... TODO
    """
    c = Cifti(parcel_labels_lr)
    pscalars_lr = map_left_to_lr(pscalars)
    c.set_cmap(pscalars_lr, cmap=cmap, vrange=vrange)
    c.save(fout)
    return


def write_dense_image(dscalars, fname):

    """
    Save dense scalars to a NIFTI neuroimaging file for visualization in
    Connnectome Workbench.

    Parameters
    ----------
    dscalars : ndarray
        scalar vector of length config.constants.N_CIFTI_INDEX
    fname : str
        Output filename, saved to outputs directory w/ extension dscalar.nii

    Returns
    -------
    f : str
        absolute path to saved file

    """

    assert dscalars.size == 91282  # TODO

    if sep in fname:
        fname = fname.split(sep)[-1]

    ext = ".dscalar.nii"
    if fname[-12:] != ext:
        assert ".nii" != fname[-4:] != ".gii"
        fname += ext

    new_data = np.copy(dscalars)

    # Load template NIFTI file (from which to create a new file)
    of = nib.load(constants.DSCALAR_FILE)

    # Load data from the template file
    temp_data = np.array(of.get_data())

    # Reshape the new data appropriately
    data_to_write = new_data.reshape(np.shape(temp_data))

    # Create and save a new NIFTI2 image object
    new_img = nib.Nifti2Image(
        data_to_write, affine=of.affine, header=of.header)
    f = join(config.OUTPUT_DIR, fname)
    nib.save(new_img, f)
    return f


class Cifti(object):

    def __init__(self, fname):
        """

        Parameters
        ----------
        fname

        """
        of = nib.load(fname)
        self.data = of.get_data()
        self.affine = of.affine
        self.header = of.header

        self.vrange = None
        self.extensions = eT.fromstring(self.header.extensions[0].get_content())
        self.ischanged = False

    def set_cmap(self, data, cmap=None, vrange=None, mappable=None):
        """
        Map scalar data to RGB values using the provided colormap.

        Parameters
        ----------
        data : numpy.ndarray
        cmap : str
        vrange : tuple
        mappable

        Returns
        -------

        """

        cmap = plots.check_cmap(cmap)

        # Map data to colors
        if mappable is None:
            self.vrange = [data.min(), data.max()] if vrange is None else vrange
            cnorm = clrs.Normalize(vmin=self.vrange[0], vmax=self.vrange[1])
            clr_map = cm.ScalarMappable(cmap=cmap, norm=cnorm)
            colors = clr_map.to_rgba(data)
        else:
            colors = np.array([mappable(d) for d in data])

        # Set zero values (i.e., masked values) to grey
        greys = cm.get_cmap('Greys')
        nullmap = greys(0.2 * np.ones(np.sum(data == 0.0)))
        colors[data == 0.0, :] = nullmap

        for ii in range(1, len(self.extensions[0][1][0][1])):
            self.extensions[0][1][0][1][ii].set(
                'Red', str(colors[ii - 1, 0]))
            self.extensions[0][1][0][1][ii].set(
                'Green', str(colors[ii - 1, 1]))
            self.extensions[0][1][0][1][ii].set(
                'Blue', str(colors[ii - 1, 2]))
            self.extensions[0][1][0][1][ii].set(
                'Alpha', str(colors[ii - 1, 3]))
        self.ischanged = True

    def write_extensions(self):
        self.header.extensions[0].content = eT.tostring(self.extensions)

    def save(self, fout):
        """

        Parameters
        ----------
        fout : str
            absolute path to output file

        Returns
        -------
        None

        """
        if self.ischanged:
            self.write_extensions()
        new_img = nib.Nifti2Image(
            self.data, affine=self.affine, header=self.header)
        nib.save(new_img, fout)

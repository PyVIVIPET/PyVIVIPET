import numpy as np
import nibabel as nib


def load_nifti(path):
    """
    Load a NIfTI image and return the data array and Nibabel image object.

    Parameters
    ----------
    path : str
        Path to the NIfTI file (.nii).

    Returns
    -------
    data : np.ndarray
        The image data array, squeezed to remove singleton dimensions.
    image : nibabel.Nifti1Image
        The Nibabel image object, including header and affine information.
    """
    print(f"Loading image: {path}")
    image = nib.load(path)
    data = np.squeeze(image.get_fdata())
    return data, image


def window_level(image, center, width):
    """
    Apply window-level normalization to an image, scaling to [0, 1].

    Parameters
    ----------
    image : np.ndarray
        Input image data.
    center : float
        Window center value.
    width : float
        Window width value.

    Returns
    -------
    image_windowed : np.ndarray
        Windowed image normalized to [0, 1].
    """
    lower = center - width / 2
    upper = center + width / 2
    image_windowed = np.clip(image, lower, upper)
    return (image_windowed - lower) / width


def print_nifti_info(nifti_image, data=None, name="Image"):
    """
    Print information about a NIfTI image, including shape, voxel size,
    and optional min/max intensity values.

    Parameters
    ----------
    nifti_image : nibabel.Nifti1Image
        The loaded NIfTI image.
    data : np.ndarray, optional
        The image data array. If None, will extract from nifti_image.
    name : str
        Name of the image for printing.
    """
    if data is None:
        data = np.squeeze(nifti_image.get_fdata())

    voxel_sizes = np.abs(nifti_image.header.get_zooms()[:3])
    print(f"{name} shape: {data.shape}, voxel size: {voxel_sizes} mm, "
          f"min={data.min():.2f}, max={data.max():.2f}")


def crop_left_half_and_shift(ct_data, pet_data=None, shift_voxels=(0, 2, -7)):
    """
    Crop CT (and optionally PET) to the left sagittal half with a small margin,
    and optionally shift PET volume for alignment.

    Parameters
    ----------
    ct_data : np.ndarray
        3D CT volume array.
    pet_data : np.ndarray or None
        3D PET volume array. If None, only CT is cropped.
    shift_voxels : tuple of int, default=(0, 2, -5)
        Number of voxels to shift PET along each axis (x, y, z).

    Returns
    -------
    ct_cropped : np.ndarray
        Cropped CT volume.
    pet_cropped : np.ndarray or None
        Cropped (and shifted) PET volume if pet_data was provided; else None.
    """

    # Crop to left hemisphere + small margin
    midpoint = ct_data.shape[0] // 2
    extra = int(ct_data.shape[0] * 0.03)
    cutoff = midpoint - extra

    ct_cropped = ct_data[:cutoff, :, :]

    pet_cropped = None
    if pet_data is not None:
        pet_cropped = pet_data[:cutoff, :, :]
        # Apply shift
        pet_cropped = np.roll(pet_cropped, shift=shift_voxels, axis=(0, 1, 2))
        print(f"Applied PET alignment shift (voxels): {shift_voxels}")

    print(f"Cropped CT shape: {ct_cropped.shape}")
    if pet_cropped is not None:
        print(f"Cropped PET shape: {pet_cropped.shape}")

    return ct_cropped, pet_cropped


def mask_region(volume, center, size=(15, 15, 15), name="Region"):
    """
    Mask a cuboid region in a 3D volume by setting it to zero.
    This is useful for removing artifacts or unwanted hotspots (e.g. bladder in animal PET scan).

    Parameters
    ----------
    volume : np.ndarray
        3D volume data (e.g., PET) to be masked.
    center : tuple of int (x, y, z)
        Center coordinates of the region to mask.
    size : tuple of int, default=(15, 15, 15)
        Half-size of the cuboid region in voxels along each axis (dx, dy, dz).
    name : str, default="Region"
        Name of the masked region, used for printing.

    Returns
    -------
    masked_volume : np.ndarray
        Copy of the input volume with the specified region set to zero.
    """

    masked_volume = volume.copy()
    x_center, y_center, z_center = center
    dx, dy, dz = size

    # Compute bounding box and clip to volume bounds
    x_start, x_end = max(0, x_center - dx), min(volume.shape[0], x_center + dx)
    y_start, y_end = max(0, y_center - dy), min(volume.shape[1], y_center + dy)
    z_start, z_end = max(0, z_center - dz), min(volume.shape[2], z_center + dz)

    masked_volume[int(x_start):int(x_end),
                  int(y_start):int(y_end),
                  int(z_start):int(z_end)] = 0

    print(f"{name} masked: x=({x_start},{x_end}), y=({y_start},{y_end}), z=({z_start},{z_end})")
    return masked_volume

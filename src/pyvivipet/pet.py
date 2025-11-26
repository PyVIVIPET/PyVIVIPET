import numpy as np
import nibabel as nib
from nibabel.processing import resample_from_to


def resample_pet_to_ct(pet_data, pet_image, ct_data, ct_image, ct_factor):
    print("Resampling PET to CT grid...")
    ct_affine = ct_image.affine.copy()
    ct_affine[:3, :3] *= ct_factor
    ct_ds_image = nib.Nifti1Image(ct_data, affine=ct_affine)

    pet_image_clean = nib.Nifti1Image(pet_data, affine=pet_image.affine)
    pet_resampled = resample_from_to(pet_image_clean, ct_ds_image, order=1)
    return pet_resampled.get_fdata()


def window_pet(pet):
    # Remove extreme hot spots
    pet_min = 1
    pet_max = np.percentile(pet, 99.9)
    print(f"PET window: min={pet_min}, max={pet_max}")
    # Values below pet_min become 0, values above pet_max become 1
    pet_windowed = np.clip(pet, pet_min, pet_max)
    pet_windowed = (pet_windowed - pet_min) / (pet_max - pet_min)

    mask = pet_windowed > 0.3
    return pet_windowed * mask


def shift_pet(pet, shift):
    print(f"Applying PET shift {shift}...")
    return np.roll(pet, shift=shift, axis=(0, 1, 2))

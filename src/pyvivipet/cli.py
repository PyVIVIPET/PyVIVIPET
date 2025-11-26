import argparse

from .utils import load_nifti, print_nifti_info, crop_left_half_and_shift, mask_region
from .ct import downsample_ct, apply_ct_window
from .pet import resample_pet_to_ct, window_pet, shift_pet
from .viewer import visualize


def main():
    parser = argparse.ArgumentParser(description="PyVIVIPET — PET/CT viewer")

    parser.add_argument("--ct", type=str, help="Path to CT .nii")
    parser.add_argument("--pet", type=str, help="Path to PET .nii")
    parser.add_argument("--ct-window", type=str, default="animal")
    parser.add_argument("--downsample", type=int, default=2)
    # Bladder masking (optional)
    parser.add_argument("--remove-bladder", action="store_true", help="Remove bladder region from PET before visualization")

    args = parser.parse_args()

    ct_data = None
    pet_data = None

    # Load CT
    if args.ct:
        ct_raw, ct_image = load_nifti(args.ct)
        print_nifti_info(ct_image, ct_raw, name="CT")
        ct_data = downsample_ct(ct_raw, args.downsample)

    # Load PET
    if args.pet:
        pet_raw, pet_image = load_nifti(args.pet)
        print_nifti_info(pet_image, pet_raw, name="PET")

        if ct_data is not None:
            pet_data = resample_pet_to_ct(pet_raw, pet_image, ct_data, ct_image, args.downsample)
            ct_data, pet_data = crop_left_half_and_shift(ct_data, pet_data, shift_voxels=(0, 2, -7))
            ct_data = apply_ct_window(ct_data, args.ct_window)
            pet_data = window_pet(pet_data)
        else:
            pet_data = window_pet(pet_raw)

    if args.pet and args.remove_bladder:
        bladder_center = (170, 242, 170)
        bladder_size = (30, 30, 30)
        pet_data = mask_region(pet_data, center=bladder_center, size=bladder_size, name="Bladder")

    # Visualization
    visualize(ct=ct_data, pet=pet_data)

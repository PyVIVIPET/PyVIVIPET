
# PyVIVIPET

PyVIVIPET is a Python volumetric imaging viewer for PET/CT.

The tool is an open-source volumetric visualization tool for PET/CT imaging. It allows interactive exploration of PET, CT, or fused PET–CT overlays with optional cropping, windowing, and artifact masking, using the standard medical imaging format `.nii` (NIfTI).

## Installation

First clone the repository:
```
git clone https://github.com/PyVIVIPET/PyVIVIPET
```
Create and activate a virtual environment:
```
python3 -m venv venv
source ./venv/bin/activate
```
Install the tool:
```
pip install -e .
```

The package exposes a command-line interface:
```
pyvivipet --help
```

### Required Input Files
PyVIVIPET expects two NIfTI files as input:

1. `CT.nii` as the CT volume
2. `PET.nii` as the PET volume

These can be generated or converted using tools like:

- [Dcm2niix](https://github.com/rordenlab/dcm2niix)
- [Nibabel](https://nipy.org/nibabel/) scripts
- [Amide](https://amide.sourceforge.io/)

You may use either file individually (PET-only or CT-only), or combine both for an interactive PET–CT fusion view.

## Command-Line Usage

| Argument           | Description                                               |
| ------------------ | --------------------------------------------------------- |
| `--ct`             | Path to the CT `.nii` file                                |
| `--pet`            | Path to the PET `.nii` file                               |
| `--ct-window`      | CT window preset (`soft_tissue`, `amide`, `try6`, `full`) |
| `--downsample`     | CT downsampling factor (integer)                          |
| `--pet-shift`      | Optional PET alignment shift (format: `"x,y,z"`)          |
| `--crop-mouse`     | Crop to left hemibody                                     |
| `--remove-bladder` | Mask bright bladder region in PET before visualization    |


#### Run CT-only Visualization
```
pyvivipet --ct CT.nii
```

#### Run PET-only Visualization
```
pyvivipet --pet PET.nii
```

#### Run Fused PET–CT Overlay Visualization
```
pyvivipet --ct CT.nii --pet PET.nii
```
Optional flags:

```
pyvivipet \
    --ct CT.nii \
    --pet PET.nii \
    --ct-window try6 \
    --downsample 2 \
    --remove-bladder
```

Example:
```
pyvivipet --pet PET.nii --ct CT.nii --remove-bladder
```


### Configuration Notes

#### CT Windowing
Internal presets are available for CT intensity scaling:
```
soft_tissue | amide | animal
```

#### PET Resampling

PET is automatically resampled to CT space using `nibabel.resample_from_to`.

#### Bladder Masking
Bright bladder uptake can be removed automatically with:
```
--remove-bladder
```

#### Functions
All core processing functions are available as Python helpers:
```
from pyvivipet.utils import (
    load_nifti, downsample_ct, apply_ct_window,
    resample_pet_to_ct, window_pet, shift_pet,
    crop_left_half_and_shift, mask_region
)
```

## Contributions
- C.S. Braams (Lead maintainer)
- L.M. Braams (Contributor)

Contributions are welcome! Please feel free to open an issue or submit a pull request on the GitHub repository.

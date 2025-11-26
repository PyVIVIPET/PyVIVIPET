import numpy as np
from skimage.measure import block_reduce
from .utils import window_level

WINDOW_PRESETS = {
    'soft_tissue': {'center': 40, 'width': 400},
    'amide': {'center': 450, 'width': 1500},
    'animal': {'center': 650, 'width': 540},
}

def downsample_ct(ct_data, factor):
    return block_reduce(ct_data, block_size=(factor, factor, factor), func=np.mean)


def apply_ct_window(ct_data, preset_name='animal'):
    preset = WINDOW_PRESETS.get(preset_name)
    if preset is None:
        raise ValueError(f"Unknown CT window preset: {preset_name}")
    center = preset["center"]
    width = preset["width"]

    return window_level(ct_data, center, width)

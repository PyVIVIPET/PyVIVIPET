import numpy as np
import pyvista as pv


def visualize(ct=None, pet=None):
    plotter = pv.Plotter()

    if ct is not None:
        plotter.add_volume(
            pv.wrap(ct),
            cmap="bone",
            opacity="linear",
            blending="composite",
            clim=[0, 1]
        )

    if pet is not None:
        opacity_values = np.linspace(0, 0.09, 20)
        plotter.add_volume(
            pv.wrap(pet),
            cmap="inferno",
            opacity=opacity_values.tolist(),
            blending="composite",
            clim=[0, 1]
        )

    print("Launching pyvista plot...")
    plotter.show()

import numpy as np
import pyvista as pv

def visualize(ct=None, pet=None, filename="rotation.mp4", n_frames=600):
    plotter = pv.Plotter(off_screen=True, window_size=(1920, 1080))

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

    plotter.remove_scalar_bar()

    # Shifted z - center a bit higher (blatter info; 250 + 20)
    x_center, y_center, z_center = 170, 242, 270
    center = np.array([x_center, y_center, z_center])

    # Initialize camera and render once
    plotter.show(auto_close=False)
    plotter.camera.Zoom(1.4)
    plotter.open_movie(filename, framerate=30)


    # Get initial camera vector relative to center
    cam_vec = np.array(plotter.camera_position[0]) - center
    radius = np.linalg.norm(cam_vec)

    # Tilt in radians
    tilt_angle=15
    tilt_rad = np.radians(tilt_angle)

    for i in range(n_frames):
        theta = 2 * np.pi * i / n_frames
        # Tilted orbit coordinates
        x = radius * np.cos(theta)
        y = radius * np.sin(theta) * np.cos(tilt_rad)
        z = radius * np.sin(theta) * np.sin(tilt_rad)
        plotter.camera_position = [
            (x + center[0], y + center[1], z + center[2]), center, (0, 0, 1)
        ]
        plotter.write_frame()


    plotter.close()
    print(f"Saved movie to {filename}")


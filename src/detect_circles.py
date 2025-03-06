import logging
import os

import click
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from skimage.transform import hough_circle, hough_circle_peaks

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


@click.command()
@click.option("--image_dir", default="images", help="Directory containing images.")
@click.option("--output_dir", default="tests", help="Directory to save processed images.")
@click.option("--blur_ksize", default=11, help="Kernel size for Gaussian blur (must be odd).")
@click.option("--canny_threshold1", default=25, help="First threshold for Canny edge detection.")
@click.option("--canny_threshold2", default=150, help="Second threshold for Canny edge detection.")
@click.option("--min_radius", default=100, help="Minimum radius for Hough Circle Transform.")
@click.option("--max_radius", default=200, help="Maximum radius for Hough Circle Transform.")
@click.option("--radius_step", default=2, help="Step size for radius range in Hough Transform.")
@click.option("--hough_threshold_factor", default=0.45, help="Factor to determine Hough Transform threshold.")
@click.option("--min_xdistance", default=40, help="Min distance between detected circle centers (x-axis).")
@click.option("--min_ydistance", default=40, help="Min distance between detected circle centers (y-axis).")
def detect_circles(
    image_dir,
    output_dir,
    blur_ksize,
    canny_threshold1,
    canny_threshold2,
    min_radius,
    max_radius,
    radius_step,
    hough_threshold_factor,
    min_xdistance,
    min_ydistance,
):
    """Detect circles in images using Hough Transform and save results."""

    try:
        image_files = os.listdir(image_dir)
    except FileNotFoundError:
        logger.error(f"The directory '{image_dir}' does not exist.")
        return

    try:
        os.makedirs(output_dir, exist_ok=True)
    except Exception as e:
        logger.error(f"Failed to create output directory '{output_dir}': {e}")
        return

    if not image_files:
        logger.error(f"No images found in '{image_dir}'.")
        return

    for image in image_files:
        image_path = os.path.join(image_dir, image)
        loaded_image = cv.imread(image_path)

        if loaded_image is None:
            logger.warning(f"Could not read {image}. Skipping...")
            continue

        image_name = os.path.splitext(image)[0]

        # Convert to grayscale
        gray = cv.cvtColor(loaded_image, cv.COLOR_BGR2GRAY)

        # Apply Gaussian blur (ensure kernel size is odd)
        blur_ksize = blur_ksize + 1 if blur_ksize % 2 == 0 else blur_ksize
        gaussian = cv.GaussianBlur(gray, (blur_ksize, blur_ksize), 0)

        # Canny edge detection
        edges = cv.Canny(gaussian, canny_threshold1, canny_threshold2)

        logger.info(f"Detecting circles in {image}")

        # Define range of radii
        radii_range = np.arange(min_radius, max_radius, radius_step)

        # Apply Hough Transform
        hough_result = hough_circle(edges, radii_range)
        hough_threshold = hough_threshold_factor * np.max(hough_result)

        # Extract circles
        _, cx, cy, radii = hough_circle_peaks(
            hough_result,
            radii_range,
            min_xdistance=min_xdistance,
            min_ydistance=min_ydistance,
            threshold=hough_threshold,
        )

        # Visualization setup
        fig, axes = plt.subplots(1, 3, figsize=(20, 10), facecolor="darkturquoise")
        fig.subplots_adjust(wspace=0.1)

        # Draw detected circles on the image
        output = loaded_image.copy()
        for x, y, r in zip(cx, cy, radii):
            cv.circle(output, (x, y), r, (0, 255, 0), 3)
            cv.circle(output, (x, y), 2, (0, 255, 255), 20)

        # Convert images to RGB for proper visualization
        loaded_image_rgb = cv.cvtColor(loaded_image, cv.COLOR_BGR2RGB)
        output_rgb = cv.cvtColor(output, cv.COLOR_BGR2RGB)

        # Display images
        images = [loaded_image_rgb, edges, output_rgb]
        titles = ["Original Image", "Detected Edges", "Detected Circles"]
        for ax, img, title in zip(axes, images, titles):
            ax.imshow(img, cmap="gray" if title == "Detected Edges" else None)
            ax.set_title(title, fontdict={"family": "serif", "color": "black", "size": 20})
            ax.set_axis_off()

        # Save the output figure
        output_path = os.path.join(output_dir, f"{image_name}.jpeg")
        fig.savefig(output_path, dpi=300, facecolor=fig.get_facecolor(), bbox_inches="tight")
        logger.info(f"Saved results to {output_path}")


if __name__ == "__main__":
    detect_circles()

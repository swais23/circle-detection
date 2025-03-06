# Circle Detection

This project detects circular objects (such as coins) in images using OpenCV and the Hough Circle Transform. It provides a minimal yet flexible setup using Docker, `click` for CLI argument management, and a Makefile for ease of use.

## Setup

### 1. Build the Docker Image

```sh
make build
```

This builds the `circle-detection` service defined in `docker-compose.yaml`.

### 2. Run the Application

```sh
make run
```

This starts a temporary container with the application.

### 3. Compile Dependencies

If you need to update `requirements.txt`, run:

```sh
make compile-requirements
```

## **Using the Circle Detection Script**

The main script for detecting circles is located in `src/detect_circles.py`. It allows parameter customization using CLI arguments.

### **Running the Script**

Once inside the container, execute the following command to detect circles in images:
```sh
python detect_circles.py --image_dir images --output_dir processed-images \
    --blur_ksize 11 --canny_threshold1 25 --canny_threshold2 150 \
    --min_radius 100 --max_radius 200 --radius_step 2 \
    --hough_threshold_factor 0.45 --min_xdistance 40 --min_ydistance 40
```

### **Explanation of Arguments:**

- `--image_dir`: Directory containing input images (default: `images/`)
- `--output_dir`: Directory to save processed images (default: `processed-images/`)
- `--blur_ksize`: Kernel size for Gaussian blur (must be odd, default: `11`)
- `--canny_threshold1`: First threshold for Canny edge detection (default: `25`)
- `--canny_threshold2`: Second threshold for Canny edge detection (default: `150`)
- `--min_radius`: Minimum circle radius for Hough Transform (default: `100`)
- `--max_radius`: Maximum circle radius for Hough Transform (default: `200`)
- `--radius_step`: Step size for radius range (default: `2`)
- `--hough_threshold_factor`: Factor to determine Hough Transform threshold (default: `0.45`)
- `--min_xdistance`: Minimum x distance between detected circles (default: `40`)
- `--min_ydistance`: Minimum y distance between detected circles (default: `40`)

## **Project Structure**

```
├── Dockerfile
├── docker-compose.yaml
├── Makefile
├── images/               # Directory containing input images
├── processed-images/     # Output directory for processed images
├── requirements/         # Dependencies
│   ├── requirements.in
|   ├── requirements.txt
├── src/
│   ├── detect_circles.py # Main script for circle detection
├── README.md
```
# Live Image Processing Web App

A Streamlit web app that applies classical image processing filters to uploaded images, with a side-by-side view of the original and the result.

**Live demo:** https://bhavya-image-filters.streamlit.app

## Features
- Upload JPG or PNG images (large images are downscaled automatically)
- Filters: grayscale, Gaussian smoothing, sharpening, Canny edge detection
- Adjustable parameters: kernel size and sigma for smoothing, low and high thresholds for edge detection
- Download the processed image

## How it works
- **Grayscale:** converts the image from BGR to a single intensity channel.
- **Smoothing:** applies a Gaussian blur with a configurable kernel size and sigma to reduce noise.
- **Sharpening:** convolves the image with a 3x3 sharpening kernel to emphasize edges and detail.
- **Edge detection:** runs the Canny algorithm on the grayscale image. Pixels above the high threshold are strong edges, and pixels between the two thresholds are kept only if they connect to strong edges.

## Tech stack
Python, OpenCV, NumPy, Pillow, Streamlit. Deployed on Streamlit Community Cloud.

## Run locally
    git clone https://github.com/bhavya-dadhich22/image-filtering-app.git
    cd image-filtering-app
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    streamlit run app.py

## Limitations and next steps
- Filters are classical, hand-written operations, not learned models.
- Possible extensions: object detection or defect detection with a trained model, and batch processing of multiple images.
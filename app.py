import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="Live Image Processing Web App", page_icon="🖼️", layout="wide")
st.title("Live Image Processing Web App")

uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
filter_name = st.selectbox(
    "Choose a filter to apply",
    ["None", "Grayscale", "Smoothing", "Sharpening", "Edge Detection"]
)

if uploaded:
    pil_img = Image.open(uploaded).convert("RGB")
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(pil_img, use_container_width=True)

    processed = img.copy()

    if filter_name == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filter_name == "Smoothing":
        processed = cv2.GaussianBlur(img, (7, 7), 1.2)
    elif filter_name == "Sharpening":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        processed = cv2.filter2D(img, -1, kernel)
    elif filter_name == "Edge Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        processed = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    processed_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)

    with col2:
        st.subheader(filter_name if filter_name != "None" else "No Filter")
        st.image(processed_rgb, use_container_width=True)
else:
    st.info("Upload an image to begin.")


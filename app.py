import cv2
import numpy as np
import streamlit as st
from PIL import Image

MAX_SIDE = 1600  # resize large images so the app stays fast

st.set_page_config(page_title="Live Image Processing Web App", page_icon="🖼️", layout="wide")
st.title("Live Image Processing Web App")


def load_image(file):
    """Read an uploaded file and return a BGR image, downscaled if very large."""
    pil_img = Image.open(file).convert("RGB")
    img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    h, w = img.shape[:2]
    scale = MAX_SIDE / max(h, w)
    if scale < 1:
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
    return img


def apply_filter(img, name, ksize=7, sigma=1.2, low=100, high=200):
    """Apply the selected filter to a BGR image and return a 3-channel BGR image."""
    if name == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    if name == "Smoothing":
        return cv2.GaussianBlur(img, (ksize, ksize), sigma)
    if name == "Sharpening":
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        return cv2.filter2D(img, -1, kernel)
    if name == "Edge Detection":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, low, high)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    return img.copy()


uploaded = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
filter_name = st.selectbox(
    "Choose a filter to apply",
    ["None", "Grayscale", "Smoothing", "Sharpening", "Edge Detection"],
)


params = {}
if filter_name == "Smoothing":
    params["ksize"] = st.slider("Kernel size (odd)", 3, 15, 7, step=2)
    params["sigma"] = st.slider("Sigma", 0.1, 5.0, 1.2, step=0.1)
elif filter_name == "Edge Detection":
    params["low"] = st.slider("Canny low threshold", 0, 255, 100)
    params["high"] = st.slider("Canny high threshold", 0, 255, 200)

if uploaded:
    try:
        img = load_image(uploaded)
    except Exception:
        st.error("Could not read that image. Please upload a valid JPG or PNG.")
        st.stop()
    if filter_name == "Edge Detection" and params["low"] > params["high"]:
        st.warning("Low threshold should be lower than the high threshold.")
    processed = apply_filter(img, filter_name, **params)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original")
        st.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), use_container_width=True)
    with col2:
        st.subheader(filter_name if filter_name != "None" else "No Filter")
        st.image(cv2.cvtColor(processed, cv2.COLOR_BGR2RGB), use_container_width=True)

    ok, buf = cv2.imencode(".png", processed)
    if ok:
        st.download_button(
            "Download processed image",
            data=buf.tobytes(),
            file_name=f"{filter_name.lower().replace(' ', '_')}.png",
            mime="image/png",
        )
else:
    st.info("Upload an image to begin.")
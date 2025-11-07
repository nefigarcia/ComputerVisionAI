import cv2
import numpy as np
import time
import streamlit as st

# Your IP camera URL
CAM_URL = "https://public.ivideon.com/camera/100-FYW8wCUjdsxJjRv8myRhCX/0/"

# Dummy defect detection function (replace with your ML model)
def detect_defects(frame):
    h, w, _ = frame.shape
    # Draw a random rectangle to simulate defect detection
    x1, y1 = np.random.randint(0, w//2), np.random.randint(0, h//2)
    x2, y2 = np.random.randint(w//2, w), np.random.randint(h//2, h)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
    return frame, {"defects": 1}

# Streamlit app
st.title("📹 Real-time Defect Detection Dashboard")

# Layout: video on left, stats on right
col1, col2 = st.columns([3, 1])
frame_placeholder = col1.empty()
stats_placeholder = col2.empty()

# Connect to your IP camera
cap = cv2.VideoCapture(CAM_URL)

if not cap.isOpened():
    st.error("❌ Cannot open IP camera. Check the URL and that the phone app is running.")
else:
    defect_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            st.warning("⚠️ No frame received from IP camera.")
            break

        # Run detection
        processed, stats = detect_defects(frame)
        defect_count += stats["defects"]

        # Show frame (convert BGR → RGB)
        frame_rgb = cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
        frame_placeholder.image(frame_rgb, channels="RGB")

        # Show stats
        stats_placeholder.metric("Defects detected", defect_count)

        time.sleep(0.1)

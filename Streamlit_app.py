# import cv2
# import streamlit as st
# from PIL import Image
# # from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
# # RTC_CONFIGURATION = {
# #     "iceServers": [
# #         {"urls": ["stun:stun.l.google.com:19302"]},
# #         {"urls": ["stun:stun1.l.google.com:19302"]},
# #     ]
# # }

# RESIZE_WIDTH = 500
# RESIZE_HEIGHT = 300


# def process_uploaded_image(uploaded_file):
#     if uploaded_file is not None:
#         image = Image.open(uploaded_file)
#         # Convert RGBA to RGB if image has an alpha channel
#         if image.mode == 'RGBA':
#             image = image.convert('RGB')

#         image = image.resize((RESIZE_WIDTH, RESIZE_HEIGHT))
#         image_path = "uploaded_image.jpg"  # Save the resized image to a file
#         image.save(image_path)
#         return image_path
#     return None



# def process_camera_snapshot():
#     video_capture = cv2.VideoCapture(0)
#     ret, frame = video_capture.read()
#     if ret:
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         image = Image.fromarray(frame)
#         image = image.resize((RESIZE_WIDTH, RESIZE_HEIGHT))
#         snapshot_path = "snapshot.jpg"  # Save the resized snapshot image to a file
#         image.save(snapshot_path)
#         return snapshot_path
#     return None
    
# # webrtc_ctx = webrtc_streamer(
# #     key="WYH",
# #     mode=WebRtcMode.SENDRECV,
# #     rtc_configuration=RTC_CONFIGURATION,
# #     media_stream_constraints={"video": True, "audio": False},
# #     async_processing=True,
# # )

# def main():
#     # image = Image.open('https://github.com/AbQadirr/CI_APP/blob/main/MediTi.png')
#     # st.image(
#     #         image,
#     #         width=400, # Manually Adjust the width of the image as per requirement
#     #     )

#     st.title("Image Comparing Streamlit App")

#     col1, col2 = st.columns(2)

#     image_path = None  # Initialize image_path variable
#     snapshot_path = None  # Initialize snapshot_path variable

    
#     # Add the logo image
    

#     with col1:
#         st.subheader("Upload an Image")
#         uploaded_file = st.file_uploader("&nbsp;", type=["jpg", "jpeg", "png"], accept_multiple_files=False, help="", label_visibility='visible')
#         if uploaded_file is not None:
#             image_path = process_uploaded_image(uploaded_file)

#     with col2:
#         st.subheader("Camera Snapshot")
#         snapshot_button = st.button("Take Snapshot")
#         if snapshot_button:
#             snapshot_path = process_camera_snapshot()

#     # Show both images in a balanced manner
#     if image_path is not None and snapshot_path is not None:
#         st.subheader("Images")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.image(image_path, caption="Uploaded Image")
#         with col2:
#             st.image(snapshot_path, caption="Snapshot")    







#     # Perform image comparison and print the result
#     if image_path and snapshot_path:
#         image1 = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
#         image2 = cv2.imread(snapshot_path, cv2.IMREAD_GRAYSCALE)
     
#         image1 = cv2.resize(image1, (RESIZE_WIDTH, RESIZE_HEIGHT))
#         image2= cv2.resize(image2, (RESIZE_WIDTH, RESIZE_HEIGHT))


#         # Initialize ORBimage1.shape == image2.shape:
#         orb = cv2.ORB_create()

#         # Detect keypoints and compute descriptors
#         keypoints1, descriptors1 = orb.detectAndCompute(image1, None)
#         keypoints2, descriptors2 = orb.detectAndCompute(image2, None)


#         # Create a BFMatcher object
#         matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
#         matches = matcher.knnMatch(descriptors1, descriptors2, k=2)

     

#         # Filter good matches
#         good_matches = []
#         for m, n in matches:
#             if m.distance < 0.7 * n.distance:
#                 good_matches.append([m])

#         # Draw the matches
#         final_image = cv2.drawMatchesKnn(image1, keypoints1, image2, keypoints2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
#         threshold = 10

#         if len(good_matches) >= threshold:
#             st.markdown("<div style='text-align: center; background-color: white; padding: 5px; border-radius: 5px'><strong><span style='color: black'>Images are the Match.</span></strong></div>", unsafe_allow_html=True)
#             # st.write("Images are  the same.")
#         else:
#             st.markdown(f"<div style='display: flex; justify-content: center;'><div style='text-align: center; background-color: white; padding: 5px 20px; border-radius: 5px; max-width: {200}px'><strong><span style='color: black'>Images doesn't Match.</span></strong></div></div>", unsafe_allow_html=True)
#             # st.write("Images are different.")

import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

# Define RESIZE_WIDTH and RESIZE_HEIGHT according to your requirements
RESIZE_WIDTH = 640
RESIZE_HEIGHT = 480

class SnapshotTransformer(VideoTransformerBase):
    def transform(self, frame):
        image = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (RESIZE_WIDTH, RESIZE_HEIGHT))
        return image

def main():
    st.title("Webcam Snapshot Capture")

    webrtc_ctx = webrtc_streamer(
        key="unique_snapshot_key",  # Modify the key to make it unique
        video_transformer_factory=SnapshotTransformer,
        async_transform=False,
    )

    if webrtc_ctx.video_transformer:
        if st.button("Capture Snapshot"):
            snapshot_path = "snapshot.jpg"
            image = webrtc_ctx.video_transformer.last_frame
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(snapshot_path, image)
            st.success("Snapshot captured and saved as 'snapshot.jpg'")
            st.image(image, channels="BGR", caption="Captured Snapshot")

if __name__ == "__main__":
    main()



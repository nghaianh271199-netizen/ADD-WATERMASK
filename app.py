import streamlit as st
from moviepy.editor import VideoFileClip, ImageClip, TextClip, CompositeVideoClip

st.title("🏃‍♂️ Thêm Watermark (Ảnh hoặc Chữ) chạy khắp video")

# Upload video
video_file = st.file_uploader("Chọn video (MP4/MOV)", type=["mp4", "mov"])

# Chọn loại watermark
wm_type = st.radio("Chọn loại watermark", ["Ảnh (PNG)", "Text"])

logo_file = None
wm_text = ""

if wm_type == "Ảnh (PNG)":
    logo_file = st.file_uploader("Chọn watermark (PNG)", type=["png"])
elif wm_type == "Text":
    wm_text = st.text_input("Nhập chữ watermark", "© Trung")

if video_file and (logo_file or wm_text):
    if st.button("Tạo video"):
        # Lưu video tạm
        with open("temp_video.mp4", "wb") as f:
            f.write(video_file.read())

        # Load video gốc
        clip = VideoFileClip("temp_video.mp4")

        # Tạo watermark
        if wm_type == "Ảnh (PNG)" and logo_file:
            with open("temp_logo.png", "wb") as f:
                f.write(logo_file.read())
            wm = ImageClip("temp_logo.png").set_duration(clip.duration).resize(height=60)
        else:
            wm = TextClip(
                wm_text,
                fontsize=40,
                color="white",
                font="Arial-Bold"
            ).set_duration(clip.duration)

        # Hàm di chuyển watermark
        def move_wm(t):
            x = int((clip.w + wm.w) * (t / clip.duration)) % (clip.w + wm.w) - wm.w
            y = clip.h - wm.h - 20
            return (x, y)

        wm = wm.set_pos(move_wm)

        # Ghép watermark vào video
        final = CompositeVideoClip([clip, wm])
        output_file = "output.mp4"
        final.write_videofile(output_file, codec="libx264")

        # Cho tải file kết quả
        with open(output_file, "rb") as f:
            st.download_button("📥 Tải video có watermark", f, file_name="watermarked.mp4")

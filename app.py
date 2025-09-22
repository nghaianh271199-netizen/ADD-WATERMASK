import streamlit as st
from moviepy.editor import VideoClip, ImageClip, TextClip, CompositeVideoClip, ColorClip
import numpy as np
import random
import tempfile

DURATION = 300  # 5 phút = 300 giây
W, H = 1280, 720  # độ phân giải video

# Hàm sinh vị trí random cho watermark
def random_position_generator(W, H, wm_w, wm_h, duration, step=2):
    positions = {}
    t = 0
    while t < duration:
        x = random.randint(0, max(0, W - wm_w))
        y = random.randint(0, max(0, H - wm_h))
        positions[int(t)] = (x, y)
        t += step

    def pos_func(t):
        key = int(t // step * step)
        return positions.get(key, (0, 0))
    return pos_func

def create_video(wm_type="Text", wm_input="© Trung", output_path="output.mp4"):
    # nền xanh
    bg = ColorClip(size=(W, H), color=(0, 255, 0), duration=DURATION)

    # watermark
    if wm_type == "Text":
        wm = TextClip(wm_input, fontsize=60, color="white").set_duration(DURATION)
    else:  # logo PNG
        wm = ImageClip(wm_input).set_duration(DURATION).resize(height=100)

    # độ mờ 50%
    wm = wm.set_opacity(0.5)

    # tạo vị trí random
    pos_func = random_position_generator(W, H, wm.w, wm.h, DURATION)

    wm = wm.set_pos(pos_func)

    final = CompositeVideoClip([bg, wm])
    final.write_videofile(output_path, codec="libx264", fps=24)

    return output_path

# ------------------ STREAMLIT UI ------------------
st.title("💧 Video nền xanh + Watermark random")

wm_type = st.radio("Chọn loại watermark:", ["Text", "Logo (PNG)"])

if wm_type == "Text":
    wm_text = st.text_input("✍️ Nhập watermark text:", "© Trung")
    if st.button("Tạo video"):
        output_path = "output.mp4"
        create_video("Text", wm_text, output_path)
        st.video(output_path)
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Tải video", f, "green_watermarked.mp4")

else:
    wm_logo = st.file_uploader("📂 Tải lên logo PNG", type=["png"])
    if wm_logo and st.button("Tạo video"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
            tmp_logo.write(wm_logo.read())
            logo_path = tmp_logo.name
        output_path = "output.mp4"
        create_video("Logo", logo_path, output_path)
        st.video(output_path)
        with open(output_path, "rb") as f:
            st.download_button("⬇️ Tải video", f, "green_watermarked.mp4")

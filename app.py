import streamlit as st
from moviepy.editor import (
    ImageClip,
    CompositeVideoClip,
    ColorClip
)
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont

# Thời lượng video
DURATION = 300  # 5 phút
WIDTH, HEIGHT = 1280, 720


def create_video(wm_type, wm_input, output_path):
    # Tạo nền phông xanh
    background = ColorClip(size=(WIDTH, HEIGHT), color=(0, 255, 0)).set_duration(DURATION)

    # Tạo watermark
    if wm_type == "Text":
        # tạo ảnh trong suốt
        img = Image.new("RGBA", (400, 100), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
        except:
            font = ImageFont.load_default()

        draw.text((10, 10), wm_input, font=font, fill=(255, 255, 255, 180))  # chữ trắng mờ

        wm = ImageClip(np.array(img)).set_duration(DURATION)

    else:  # logo PNG
        wm = ImageClip(wm_input).set_duration(DURATION).resize(height=100).set_opacity(0.5)

    # Random vị trí watermark chạy khắp màn hình
    def make_frame(t):
        x = random.randint(0, WIDTH - int(wm.w))
        y = random.randint(0, HEIGHT - int(wm.h))
        return (x, y)

    wm = wm.set_position(make_frame)

    # Xuất video
    final = CompositeVideoClip([background, wm])
    final.write_videofile(output_path, fps=24, codec="libx264")


# -------------------- Streamlit UI --------------------
st.title("🎥 Tạo Video Watermark 5 phút")

option = st.radio("Chọn loại watermark:", ["Text", "PNG"])

if option == "Text":
    wm_text = st.text_input("Nhập nội dung watermark:")
else:
    wm_file = st.file_uploader("Tải lên logo PNG:", type=["png"])

if st.button("Tạo Video"):
    output_path = "output.mp4"

    if option == "Text" and wm_text.strip() != "":
        create_video("Text", wm_text, output_path)
        st.success("✅ Tạo video thành công!")
        st.video(output_path)

    elif option == "PNG" and wm_file is not None:
        # Lưu file PNG tạm
        with open("wm.png", "wb") as f:
            f.write(wm_file.read())
        create_video("PNG", "wm.png", output_path)
        st.success("✅ Tạo video thành công!")
        st.video(output_path)

    else:
        st.error("❌ Vui lòng nhập text hoặc tải ảnh PNG!")

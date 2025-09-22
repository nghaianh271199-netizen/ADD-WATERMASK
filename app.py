import streamlit as st
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import tempfile

# Hàm thêm watermark dạng text
def add_text_watermark(video_path, text, output_path):
    clip = VideoFileClip(video_path)

    # Lấy kích thước video
    W, H = clip.size

    # Tạo ảnh trong suốt bằng Pillow
    txt_img = Image.new("RGBA", (W, H), (0,0,0,0))
    draw = ImageDraw.Draw(txt_img)

    # Font chữ (Streamlit Cloud có sẵn DejaVuSans)
    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except:
        font = ImageFont.load_default()

    # Vẽ chữ ở góc phải dưới
    text_w, text_h = draw.textsize(text, font=font)
    draw.text((W-text_w-20, H-text_h-20), text, font=font, fill=(255,255,255,180))

    # Convert sang ImageClip
    txt_clip = ImageClip(txt_img).set_duration(clip.duration)

    # Overlay
    final = CompositeVideoClip([clip, txt_clip])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

# Hàm thêm watermark dạng logo PNG
def add_logo_watermark(video_path, logo_path, output_path):
    clip = VideoFileClip(video_path)
    logo = (ImageClip(logo_path)
            .set_duration(clip.duration)
            .resize(height=50)  # thu nhỏ logo
            .margin(right=20, bottom=20, opacity=0)  # cách mép
            .set_pos(("right","bottom")))
    
    final = CompositeVideoClip([clip, logo])
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

# ----------------- Streamlit UI -----------------
st.title("💧 Thêm Watermark vào Video")

uploaded_video = st.file_uploader("📂 Tải lên video", type=["mp4","mov","avi"])
watermark_type = st.radio("Chọn loại watermark:", ["Text","Logo"])

if uploaded_video:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
        tmp_video.write(uploaded_video.read())
        video_path = tmp_video.name

    if watermark_type == "Text":
        wm_text = st.text_input("✍️ Nhập watermark text:")
        if st.button("Tạo video"):
            output_path = "output.mp4"
            add_text_watermark(video_path, wm_text, output_path)
            st.video(output_path)
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Tải video", f, "watermarked.mp4")
    else:
        wm_logo = st.file_uploader("📂 Tải lên logo PNG", type=["png"])
        if wm_logo and st.button("Tạo video"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_logo:
                tmp_logo.write(wm_logo.read())
                logo_path = tmp_logo.name

            output_path = "output.mp4"
            add_logo_watermark(video_path, logo_path, output_path)
            st.video(output_path)
            with open(output_path, "rb") as f:
                st.download_button("⬇️ Tải video", f, "watermarked.mp4")

import streamlit as st
import yt_dlp
import os
import shutil

st.set_page_config(page_title="Video Downloader", layout="centered")

# ------------------ THEME-AWARE CSS ------------------ #
st.markdown("""
<style>

/* Adaptive text */
body {
    color: #111;
}
@media (prefers-color-scheme: dark) {
    body {
        color: #fff;
    }
}

/* Input */
.stTextInput input {
    border-radius: 12px;
    padding: 10px;
}

/* Button */
.stButton button {
    border-radius: 12px;
    background: linear-gradient(90deg, #ff512f, #dd2476);
    color: white;
    font-weight: bold;
}

/* Card */
.card {
    padding: 18px;
    border-radius: 15px;
    margin-top: 20px;
    font-size: 17px;
    background: rgba(0,0,0,0.05);
}
@media (prefers-color-scheme: dark) {
    .card {
        background: rgba(255,255,255,0.08);
    }
}

/* Image */
img {
    border-radius: 15px;
    max-width: 100%;
    height: auto;
    box-shadow: 0px 6px 25px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.markdown("<h1 style='text-align:center;'>🎬 Multi Video Downloader</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Download videos from YouTube, Instagram & Facebook</p>", unsafe_allow_html=True)

# ------------------ INPUT ------------------ #
url = st.text_input("🔗 Paste your video link here")

# Create temp folder
os.makedirs("temp", exist_ok=True)

# ------------------ PLATFORM DETECTION ------------------ #
def detect_platform(url):
    if "youtube" in url or "youtu.be" in url:
        return "YouTube"
    elif "instagram" in url:
        return "Instagram"
    elif "facebook" in url:
        return "Facebook"
    return "Unknown"

# ------------------ YT-DLP OPTIONS ------------------ #
def get_ydl_opts(url):
    base = {
        'outtmpl': 'temp/%(title)s_%(id)s.%(ext)s',  # ✅ FIXED (unique filename)
        'quiet': True,
        'socket_timeout': 60,
        'retries': 10,
        'fragment_retries': 10,
        'sleep_interval': 2,
        'max_sleep_interval': 5,
        'http_headers': {'User-Agent': 'Mozilla/5.0'}
    }

    if "facebook" in url:
        base['format'] = 'best/bestvideo+bestaudio'
    elif "instagram" in url:
        base['format'] = 'best'
    else:
        base['format'] = 'best[height<=720]'

    return base

# ------------------ DOWNLOAD FUNCTION ------------------ #
def download_video(url):
    ydl_opts = get_ydl_opts(url)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)

    return info, file_path

# ------------------ MAIN BUTTON ------------------ #
if st.button("🚀 Download Now"):
    if url:

        # OPTIONAL: Clear old files (prevents clutter)
        shutil.rmtree("temp", ignore_errors=True)
        os.makedirs("temp", exist_ok=True)

        platform = detect_platform(url)

        # Platform Card
        st.markdown(
            f"""
            <div class='card'>
                📌 Platform Detected: <b>{platform}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

        if platform in ["Facebook", "Instagram"]:
            st.warning("⚠️ Only public videos are supported.")

        try:
            with st.spinner("⏳ Downloading..."):
                info, file_path = download_video(url)

            # Thumbnail
            if 'thumbnail' in info:
                st.markdown(
                    f"""
                    <div style="text-align:center;">
                        <img src="{info['thumbnail']}">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            st.success("✅ Video Ready!")

            # Read file
            with open(file_path, "rb") as f:
                video_bytes = f.read()

            # Download button
            st.download_button(
                "⬇ Download Video",
                data=video_bytes,
                file_name=os.path.basename(file_path),
                mime="video/mp4"
            )

        except Exception as e:
            st.error("❌ Download failed!")
            st.code(str(e))

# ------------------ FOOTER ------------------ #
st.markdown("""
<hr>
<p style='text-align:center; opacity:0.7;'>
Built with ❤️ using Streamlit
</p>
""", unsafe_allow_html=True)
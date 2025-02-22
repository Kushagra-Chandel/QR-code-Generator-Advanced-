import streamlit as st
import qrcode
from PIL import Image, ImageDraw
import io

# Streamlit Page Config
st.set_page_config(page_title=" Legacy QR Generator", layout="wide")

# Custom Styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #8B0000;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #A52A2A;
    }
    .stSidebar {
        background-color: #1E1E1E;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar Customization
st.sidebar.header("🎨 Customization")
qr_size = st.sidebar.slider("Select QR Size:", 100, 500, 300)
qr_color = st.sidebar.color_picker("QR Code Color", "#000000")
bg_color = st.sidebar.color_picker("Background Color", "#FFFFFF")

# New Features
apply_gradient = st.sidebar.checkbox("Apply Gradient Effect", False)
rounded_corners = st.sidebar.checkbox("Rounded QR Code", False)

# Main UI
st.title("⚔  Legacy QR Generator")
st.write("🔗 Generate stunning QR Codes with advanced customization options!")

# Input Field
text_input = st.text_input("Enter text or URL:", "")

# File Uploader for Logo (Optional)
uploaded_logo = st.file_uploader("Upload a logo (Optional)", type=["png", "jpg", "jpeg"])

# Function to Convert HEX to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Function to Blend Colors for Gradient
def blend_colors(color1, color2, factor):
    color1 = hex_to_rgb(color1)  # Convert hex to RGB
    color2 = hex_to_rgb(color2)  # Convert hex to RGB
    return tuple(int(cl * (1 - factor) + c2 * factor) for cl, c2 in zip(color1, color2))

# Function to Generate QR Code
def generate_qr(data, size, color, bg, gradient, round_corners, logo):
    qr = qrcode.QRCode(box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=color, back_color=bg).convert("RGBA")

    # Apply Gradient if Enabled
    if gradient:
        img = img.convert("RGBA")
        width, height = img.size
        gradient = Image.new("RGBA", (width, height), color=bg)

        for y in range(height):
            gradient_color = blend_colors(color, bg, y / height)
            for x in range(width):
                gradient.putpixel((x, y), gradient_color)
        
        img = Image.alpha_composite(img, gradient)

    # Apply Rounded Corners if Enabled
    if round_corners:
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle([(0, 0), img.size], radius=20, fill=255)
        img.putalpha(mask)

    # Overlay Logo if Uploaded
    if logo:
        logo = Image.open(logo).convert("RGBA")
        logo = logo.resize((size // 5, size // 5))
        img_w, img_h = img.size
        pos = ((img_w - logo.size[0]) // 2, (img_h - logo.size[1]) // 2)
        img.paste(logo, pos, logo)

    return img.resize((size, size))

# Generate QR Code Button
if st.button("Generate QR Code"):
    if not text_input:
        st.error("⚠ Please enter text or a URL!")
    else:
        qr_image = generate_qr(text_input, qr_size, qr_color, bg_color, apply_gradient, rounded_corners, uploaded_logo)
        st.image(qr_image, caption="Generated QR Code")

        # Download Button
        buf = io.BytesIO()
        qr_image.save(buf, format="PNG")
        st.download_button(label="📥 Download QR Code", data=buf.getvalue(), file_name="qr_code.png", mime="image/png")

# Branding Footer
st.markdown("---")
st.markdown(" powered by Raavans Legacy")

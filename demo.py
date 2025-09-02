
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import os

st.set_page_config(page_title="Merchandise Template Demo", layout="centered")
st.title("🛍️ AI-Powered Merchandise Template Generator")

demo_colors = ["#0A192F", "#FFFFFF", "#F9A826"]
demo_font = "Arial"
brand_name = st.text_input("Enter Brand Name", value="Your Brand")
option = st.radio("Choose Mockup Type", ["Mug", "T-Shirt"])
uploaded_logo = st.file_uploader("Optional: Upload a Logo", type=["png", "jpg", "jpeg"])

# Generate placeholder logo if none uploaded
if uploaded_logo:
    demo_logo = Image.open(uploaded_logo).convert("RGBA")
else:
    demo_logo = Image.new("RGBA", (200, 200), (249, 168, 38, 255))
    draw = ImageDraw.Draw(demo_logo)
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"
        font = ImageFont.truetype(font_path, 20)
    except OSError:
        font = ImageFont.load_default()
    draw.text((60, 90), "LOGO", font=font, fill="black")

# Mug mockup
def generate_mug_mockup(logo_img, colors, brand_name):
    mockup = Image.new("RGB", (800, 600), colors[1])
    draw = ImageDraw.Draw(mockup)
    draw.rectangle([200, 150, 600, 450], fill=colors[0])
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"
        font = ImageFont.truetype(font_path, 24)
    except OSError:
        font = ImageFont.load_default()
    draw.text((300, 200), brand_name, font=font, fill=colors[2])
    logo_img.thumbnail((150, 150))
    mockup.paste(logo_img, (325, 275), logo_img)
    output = BytesIO()
    mockup.save(output, format="PNG")
    output.seek(0)
    return output

# T-shirt mockup
def generate_tshirt_mockup(logo_img, colors, brand_name):
    tshirt = Image.new("RGB", (800, 1000), colors[1])
    draw = ImageDraw.Draw(tshirt)
    draw.rectangle([150, 200, 650, 800], fill=colors[0])  # Shirt body
    draw.rectangle([250, 100, 550, 200], fill=colors[0])  # Collar
    try:
        font_path = "C:/Windows/Fonts/arial.ttf"
        font = ImageFont.truetype(font_path, 36)
    except OSError:
        font = ImageFont.load_default()
    draw.text((300, 220), brand_name, font=font, fill=colors[2])
    logo_img.thumbnail((200, 200))
    tshirt.paste(logo_img, (300, 300), logo_img)
    output = BytesIO()
    tshirt.save(output, format="PNG")
    output.seek(0)
    return output

if st.button("Generate Mockup"):
    if option == "Mug":
        output_img = generate_mug_mockup(demo_logo, demo_colors, brand_name)
    else:
        output_img = generate_tshirt_mockup(demo_logo, demo_colors, brand_name)

    st.image(output_img, caption=f"{option} Mockup", use_column_width=True)
    b64 = base64.b64encode(output_img.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="mockup.png">📥 Download {option} Mockup</a>'
    st.markdown(href, unsafe_allow_html=True)

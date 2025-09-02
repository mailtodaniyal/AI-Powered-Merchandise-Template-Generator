import streamlit as st
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import base64
import re
import os

st.set_page_config(page_title="AI Merchandise Generator", layout="centered")
st.title("AI-Powered Merchandise Template Generator")
url = st.text_input("Enter Website URL")
generate = st.button("Generate Merchandise Template")
os.makedirs("assets", exist_ok=True)

def get_soup(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.text, "html.parser")

def extract_logo(soup, base_url):
    logos = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if src and ("logo" in src.lower()):
            if not src.startswith("http"):
                src = base_url + src if src.startswith("/") else base_url + "/" + src
            logos.append(src)
    return logos[0] if logos else None

def extract_colors(soup):
    styles = soup.find_all("style")
    color_set = set()
    for style in styles:
        if style.string:
            colors = re.findall(r"#(?:[0-9a-fA-F]{3}){1,2}", style.string)
            color_set.update(colors)
    return list(color_set)[:3] if color_set else ["#000000", "#FFFFFF", "#DDDDDD"]

def extract_fonts(soup):
    links = soup.find_all("link", href=True)
    for link in links:
        if "fonts.googleapis.com" in link["href"]:
            match = re.search(r"family=([^&:]+)", link["href"])
            if match:
                return match.group(1).replace("+", " ")
    return "Arial"

def get_screenshot(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=chrome_options)
    driver.set_window_size(1200, 800)
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()
    return Image.open(BytesIO(screenshot))

def generate_mockup(logo_url, colors, font_name):
    mockup = Image.new("RGB", (800, 600), colors[1])
    draw = ImageDraw.Draw(mockup)
    draw.rectangle([200, 150, 600, 450], fill=colors[0])
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if not os.path.exists(font_path):
        font_path = "/Library/Fonts/Arial.ttf"
    font = ImageFont.truetype(font_path, 24)
    draw.text((300, 200), "Your Brand", font=font, fill=colors[2])
    if logo_url:
        logo_resp = requests.get(logo_url)
        logo = Image.open(BytesIO(logo_resp.content)).convert("RGBA")
        logo.thumbnail((150, 150))
        mockup.paste(logo, (325, 275), logo)
    output = BytesIO()
    mockup.save(output, format="PNG")
    output.seek(0)
    return output

def get_base_url(url):
    parsed = requests.utils.urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

if generate and url:
    soup = get_soup(url)
    base_url = get_base_url(url)
    logo_url = extract_logo(soup, base_url)
    colors = extract_colors(soup)
    font_name = extract_fonts(soup)
    preview = generate_mockup(logo_url, colors, font_name)
    st.image(preview, caption="Merchandise Template", use_column_width=True)
    b64 = base64.b64encode(preview.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{b64}" download="merchandise_template.png">Download Template</a>'
    st.markdown(href, unsafe_allow_html=True)

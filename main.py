import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from linebot import LineBotApi
from linebot.models import ImageSendMessage

def capture_and_crop():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,1000")
    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://goat.pakka.ai:8008/wbgt?token=47fc5150d1ae4f1290bf43e9d4746b5e")
        driver.implicitly_wait(5)
        img = driver.get_screenshot_as_png()
        driver.quit()
        image = Image.open(BytesIO(img))
        cropped = image.crop((345, 260, 930, 580))
        return cropped
    except Exception as e:
        driver.quit()
        raise e

def draw_text(img):
    draw = ImageDraw.Draw(img)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)

    now = datetime.now()
    date_str = now.strftime("%m/%d")
    time_str = now.strftime("%H:%M")

    lines = [
        f"{date_str} 戶外作業 {time_str}",
        "熱危害：第 X 級",
        "依據熱危害等級/熱指數休息標準：",
        "全體人員，每小時休息10分鐘",
        "重體力作業，每小時需休息20分鐘",
        "請適當安排陰涼處休息、補充含鹽量水分"
    ]

    y = 10
    for line in lines:
        draw.text((10, y), line, font=font, fill="black")
        y += 25
    return img

def push_image(image_path):
    channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")

    line_bot_api = LineBotApi(channel_access_token)

    image_message = ImageSendMessage(
        original_content_url=image_path,
        preview_image_url=image_path
    )

    line_bot_api.push_message(group_id, image_message)

if __name__ == "__main__":
    img = capture_and_crop()
    img = draw_text(img)
    img.save("heat_index.png")
    print("圖片已儲存，可上傳圖床並推送")
    # push_image(...) 可接你圖床網址

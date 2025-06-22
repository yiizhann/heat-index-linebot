
import os
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from linebot import LineBotApi
from linebot.models import ImageSendMessage
from linebot.exceptions import LineBotApiError

def capture_and_crop():
    print("開始擷取頁面...")
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
        print("截圖完成")
        return cropped
    except Exception as e:
        driver.quit()
        print("擷取錯誤：", e)
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

def push_image():
    try:
        channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
        group_id = os.getenv("GROUP_ID")
        print(f"使用群組 ID: {group_id}")
        print(f"Access Token 開頭: {channel_access_token[:10]}...")

        line_bot_api = LineBotApi(channel_access_token)

        # 上傳本地圖檔到 Imgur、ImgBB、S3 等圖床會更安全，這邊假設使用 ngrok/本機 Web
        # 暫時使用 LINE 不支援本地檔案，所以用警示替代
        image_url = "https://i.imgur.com/your_test_image.png"  # 假設圖床網址

        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )

        print("開始推播訊息...")
        line_bot_api.push_message(group_id, image_message)
        print("推播成功 ✅")

    except LineBotApiError as e:
        print(f"LineBotApiError: {e.message}")
        print(f"Status Code: {e.status_code}")
        print(f"Response: {e.error.response}")
    except Exception as ex:
        print("其他錯誤：", ex)

if __name__ == "__main__":
    try:
        img = capture_and_crop()
        img = draw_text(img)
        img.save("heat_index.png")
        print("圖片儲存為 heat_index.png")
        push_image()
    except Exception as e:
        print("程式錯誤：", e)


import os
import requests
from datetime import datetime
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

LINE_TOKEN = os.getenv("LINE_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")

def capture_heat_image():
    url = "https://hiosha.osha.gov.tw/content/info/heat1.aspx"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--window-size=1280,720")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    screenshot = driver.get_screenshot_as_png()
    driver.quit()

    img = Image.open(BytesIO(screenshot))
    cropped = img.crop((345, 260, 930, 580))
    output_path = "heat_index_today.png"
    cropped.save(output_path)
    return output_path

def push_to_line(image_path):
    headers = {
        "Authorization": f"Bearer {LINE_TOKEN}"
    }
    now = datetime.now().strftime("%m/%d 戶外作業 %H:%M")
    message = '''{}\n熱危害 : 圖示如附圖\n依據熱危害等級/熱指數休息標準\n全體人員，每小時休息10分鐘\n重體力作業，每小時需休息20分鐘\n請適當安排陰涼處休息、補充含鹽量水分'''.format(now)

    files = {"imageFile": open(image_path, "rb")}
    res_img = requests.post(
        "https://notify-api.line.me/api/notify",
        headers=headers,
        data={"message": message},
        files=files
    )
    print(res_img.status_code)

if __name__ == "__main__":
    path = capture_heat_image()
    push_to_line(path)

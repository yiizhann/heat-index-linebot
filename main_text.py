import requests
from datetime import datetime
from linebot import LineBotApi
from linebot.models import TextSendMessage

# ====== LINE 設定 ======
channel_access_token = "srrZgTDwcfGjEzIT8qB2XcSXi0tJAxztqTByW9xG+ZGuhxwghOxOYIRtC8NI+jSKy9pZCD2To51Uo7H/biW94L43MMO2rpOOC/p6pZOKNWf9q/1TIUMjmOTQzKEtG84GhnTHMD4twJyO181OdetiiwdB04t89/1O/w1cDnyilFU="
group_id = "C5d6d2b9520472ccb60a1a440a6e911d9"

# ====== 取得熱危害級數 ======
def fetch_wbgt_level():
    url = "http://goat.pakka.ai:8008/wbgt?token=47fc5150d1ae4f1290bf43e9d4746b5e"
    response = requests.get(url)
    data = response.json()
    wbgt_level = data.get("wbgt_level", "未知")
    return wbgt_level

# ====== 組成訊息 ======
def build_message(wbgt_level):
    now = datetime.now()
    time_str = now.strftime("%m/%d %H:%M")
    return f"{time_str}: 熱危害:第{wbgt_level}級 請人員注意。"

# ====== 發送 LINE 訊息 ======
def push_message_to_line(text):
    line_bot_api = LineBotApi(channel_access_token)
    message = TextSendMessage(text=text)
    line_bot_api.push_message(group_id, message)

# ====== 主流程 ======
if __name__ == "__main__":
    try:
        wbgt_level = fetch_wbgt_level()
        message = build_message(wbgt_level)
        print("發送內容：", message)
        push_message_to_line(message)
    except Exception as e:
        print("程式錯誤：", e)

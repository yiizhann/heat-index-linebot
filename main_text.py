
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

def push_text_message():
    channel_access_token = os.getenv("CHANNEL_ACCESS_TOKEN")
    group_id = os.getenv("GROUP_ID")

    print(f"使用群組 ID: {group_id}")
    print(f"Access Token 開頭: {channel_access_token[:10]}...")

    try:
        line_bot_api = LineBotApi(channel_access_token)
        message = TextSendMessage(text="✅ LINE 群組推播測試成功！")
        line_bot_api.push_message(group_id, message)
        print("✅ 推播文字成功")
    except LineBotApiError as e:
        print("❌ LINE API 錯誤：", e.message)
        print(f"Status Code: {e.status_code}")
        print(f"Response: {e.error.response}")
    except Exception as ex:
        print("❌ 其他錯誤：", ex)

if __name__ == "__main__":
    push_text_message()

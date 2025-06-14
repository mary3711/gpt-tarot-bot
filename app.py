from flask import Flask, request, abort
import os
import openai
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from waitress import serve

load_dotenv()

app = Flask(__name__)

# 環境変数からトークン・シークレット・APIキーを取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    print("=== Webhook Received ===")
    print("Signature:", signature)
    print("Body:", body)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("=== Handler Error ===")
        print(e)
        abort(400)

    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print("User:", user_message)

    gpt_reply = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    reply_text = gpt_reply['choices'][0]['message']['content']
    print("GPT:", reply_text)

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )


# Render対応：waitress + ポート指定
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))


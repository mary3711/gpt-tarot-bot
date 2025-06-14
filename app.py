from flask import Flask, request, abort
import os
from openai import OpenAI
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
from waitress import serve

# 環境変数を読み込み
load_dotenv()

# Flaskアプリ初期化
app = Flask(__name__)

# 環境変数からLINE Bot・OpenAIのキーを取得
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAIクライアント初期化（最新版openai>=1.0対応）
client = OpenAI(api_key=openai_api_key)

# LINEのWebhookエンドポイント
@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    print("=== Webhook Received ===")
    print("signature:", signature)
    print("Body:", body)

    try:
        handler.handle(body, signature)
    except Exception as e:
        print("=== Handler Error ===")
        print(e)
        abort(400)

    return "OK"

# 動作確認用のルート
@app.route("/", methods=["GET"])
def index():
    return "OK", 200

# メッセージ受信時の処理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    print("=== Message Event Triggered ===")
    print("User:", user_message)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply_text = response.choices[0].message.content
        print("GPT:", reply_text)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_text)
        )
    except Exception as e:
        print("=== OpenAI Error ===")
        print(e)

# Render環境用サーバ起動
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

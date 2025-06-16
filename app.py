 from flask import Flask, request, render_template
from openai import OpenAI
import os

# Flaskアプリを作成
app = Flask(__name__)

# OpenAIのAPIキーを読み込む（環境変数から）
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ルートURLで占いBotを表示
@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        question = request.form.get("question")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content
    return render_template("index.html", reply=reply)

# アプリ起動（Render用にdebug=False）
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

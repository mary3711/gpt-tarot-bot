from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# OpenAIのAPIキーを読み込む
openai.api_key = os.getenv("OPENAI_API_KEY")

# トップページにアクセスしたときの処理
@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        question = request.form.get("question")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": question}
            ]
        )
        reply = response.choices[0].message.content
    return render_template("index.html", reply=reply)

# ローカルサーバーとして実行
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

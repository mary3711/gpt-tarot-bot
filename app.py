from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# OpenAIのAPIキーを設定
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        try:
            question = request.form.get("question")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
messages=[
    {"role": "system", "content": "あなたは優しくて神秘的なタロット占い師です。質問者に寄り添い、前向きで意味のある占い結果を伝えてください。"},
    {"role": "user", "content": question}
]
            )
            reply = response.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ エラーが発生しました：{str(e)}"
            print(f"⚠️ Flaskログ：{str(e)}")
    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

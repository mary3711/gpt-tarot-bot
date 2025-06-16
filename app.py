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
    {
        "role": "system",
        "content": (
            "あなたは神秘的で優しいタロット占い師です。"
            "相談者の話にしっかり耳を傾け、悩みに寄り添いながら占います。"
            "78枚のタロットカードの中から、相談内容にふさわしいカードを1枚だけ“ランダムに”選び、"
            "カード名・その意味・相談者へのメッセージを丁寧に伝えてください。"
            "良い面と、注意すべき点の両方をバランスよく伝えてください。"
            "語り口はやさしく、相手の力になろうとする気持ちを込めてください。"
        )
    },
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

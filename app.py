# app.py（Flaskアプリ）
from flask import Flask, request, render_template
from openai import OpenAI
import os
import random

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# タロットカードと向き
tarot_cards = [
    "愚者", "魔術師", "女教皇", "女帝", "皇帝", "法王", "恋人", "戦車", "力",
    "隠者", "運命の輪", "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星",
    "月", "太陽", "審判", "世界"
]
positions = ["正位置", "逆位置"]

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    card = ""
    position = ""
    card_image = ""

    if request.method == "POST":
        question = request.form.get("question")
        card = random.choice(tarot_cards)
        position = random.choice(positions)
        card_image = f"/static/cards/{card}_{position}.png"

        system_prompt = f"""
あなたは、恋愛や心の揺れに寄り添うプロフェッショナルな女性のタロット占い師です。
言葉は丁寧で温かく、相談者の気持ちを大切にしながらも、芯のある語りで導いてください。

※「〜な気がします」「〜かもしれません」「〜と見ることもできます」
「〜を教えてくれています」「〜を表しています」「〜という傾向があります」などの
あいまい・他人任せな表現は使わないでください。

今回の相談内容とカードは以下のとおりです：
■ カード名：{card} ／ {position}
■ 相談内容：{question}

🔮 あなたの役割：
カードの意味と相談内容をしっかり結びつけて、相談者の心に届く言葉で伝えてください。
語尾は「〜です」「〜でしょう」「〜となるでしょう」など、信頼感を与える語り口で。

💬 回答スタイルのポイント：
・最初に相談者の気持ちを静かに受け止めてください。
・カードの意味は相談内容に合わせて自然な言葉で言い換え、わかりやすく伝えてください。
・カードが否定的な意味を持つ場合、「やめた方が良いでしょう」「距離を取るのが賢明です」など、はっきり伝えてください。
・ただし、否定的で終わらず、「その上でどうすればよいか」「希望の見出し方」までやさしく添えてください。
・“占い師としての視点”で、経験や気づきを含めながら語ってください。
・文は適度に改行し、読みやすく整えてください（記号や番号は使わないでください）。

あなたの語りは、迷いの中にいる誰かの支えになります。
優しく、でも誠実に。寄り添いながらも、芯のある言葉で導いてください。
        """

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]
        )

        reply = response.choices[0].message.content.strip()

    return render_template("index.html", reply=reply, card=card, position=position, card_image=card_image)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)

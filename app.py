from flask import Flask, request, render_template
from openai import OpenAI
import os
import random

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# カード一覧
major_arcana = [
    "愚者", "魔術師", "女教皇", "女帝", "皇帝", "法王", "恋人", "戦車", "力",
    "隠者", "運命の輪", "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星",
    "月", "太陽", "審判", "世界"
]
positions = ["正位置", "逆位置"]

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    card_image = ""
    card = ""
    position = ""

    if request.method == "POST":
        try:
            question = request.form.get("question")
            selected_card = random.choice(major_arcana)
            selected_position = random.choice(positions)
            card = selected_card
            position = selected_position

            system_prompt = f"""
あなたは、恋愛や心の悩みに寄り添う、落ち着きと芯のある語り口をもつプロフェッショナルなタロット占い師です。

今から、相談者の悩みに対して「1枚引き」のタロットリーディングを行ってください。

【カード】
■ カード名：{selected_card} ／ {selected_position}

あなたの言葉は、迷いの中にいる人の心の支えになります。
カードの意味と相談者の心をしっかり結びつけて、前向きな気づきを届けてください。

🔮 あなたの役割は、以下の構成に沿って丁寧に語りましょう。

【構成】
1. 導入：相談内容に合わせて、そっと寄り添うようなやさしい一言から始めてください。
2. カードの意味を踏まえ、今の状況や気持ちを整理するように説明してください。
3. カードが示すヒントや注意点があれば、やわらかく、でも曖昧にせず伝えてください。
4. 最後は、相談者が前を向けるような、あたたかくやさしい希望の言葉でまとめてください。

💬 表現ルール：
・「〜のようです」「〜かもしれません」「〜と見ることもできます」「〜を表しています」など曖昧または型通りの表現は使わず、占い師としての視点で丁寧に自然な語り口で伝えてください。
・カードの絵柄や装飾の描写は不要です。
・否定的なカードが出た場合は、「今はおすすめできません」「立ち止まるときかもしれません」などのようにやわらかく、しかし結果を濁さず伝えてください。
・「自分を磨くといい」など一般的な助言ではなく、相談内容に合ったヒントを出してください。
・感情に寄り添いながらも、占い師としての深い洞察を感じさせる一歩踏み込んだ言葉を選んでください。
・文章は読みやすいように、適度に段落や改行を使ってください。

あなたの言葉が、そっと心に灯をともす存在になりますように。
"""

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"相談内容: {question}"}
                ]
            )

            reply = response.choices[0].message.content.strip()
            card_image = f"/static/cards/{selected_card}_{'upright' if selected_position == '正位置' else 'reversed'}.png"

        except Exception as e:
            reply = f"\u26a0\ufe0f エラーが発生しました：{str(e)}"

    return render_template("index.html", reply=reply, card_image=card_image, card=card, position=position)

if __name__ == "__main__":
    app.run(debug=True, port=10000)

from flask import Flask, request, render_template
from openai import OpenAI
import os
import random

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 大アルカナと向き
major_arcana = [
    "愚者", "魔術師", "女教皇", "女帝", "皇帝", "法王", "恋人", "戦車", "力",
    "隠者", "運命の輪", "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星",
    "月", "太陽", "審判", "世界"
]
positions = ["正位置", "逆位置"]

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    card_image_url = ""
    selected_card = ""
    selected_position = ""

    if request.method == "POST":
        try:
            question = request.form.get("question")
            selected_card = random.choice(major_arcana)
            selected_position = random.choice(positions)

            image_filename = f"{selected_card}_{selected_position}.png"
            card_image_url = f"/static/cards/{image_filename}"

            system_prompt = (
                "あなたは、恋愛や心の揺れに寄り添うプロフェッショナルな女性のタロット占い師です。\n"
                "静けさとあたたかさを兼ね備えた語り口で、相手を決して否定せず、心をそっと受け止めるように話してください。\n\n"

                "今回の相談内容と、すでに引かれているカードは以下の通りです：\n"
                f"■ カード名：{selected_card} ／ {selected_position}\n\n"

                "🔮 あなたの役割は、このカードの意味を【相談内容と深く結びつけて】解釈し、\n"
                "相談者が『恋愛・人間関係・心の悩み』について少しでも前向きな気づきを得られるようなヒントを伝えることです。\n\n"

                "💬 回答スタイルのルール：\n"
                "1. まずは相談者の悩みに静かに耳を傾け、感情に寄り添うような言葉で優しく導入してください。\n"
                "2. カードの意味は、相談内容の文脈にあわせて“噛み砕いて”説明し、カードの言葉として自然に語ってください。\n"
                "3. カードの絵柄や装飾の描写は不要です。\n"
                "4. 「〜を教えてくれています」ではなく「〜を表しています」「〜のような傾向が見られます」などの表現にしてください。\n"
                "5. ネガティブなことは絶対に断定せず、“助言”としてやわらかく添えてください。\n"
                "6. 「アドバイスとしては〜」といった形式的な枠ではなく、自然な会話調で穏やかに伝えてください。\n"
                "7. 最後は、相談者が心を軽くできるように、“希望を感じる言葉”でまとめてください。\n\n"

                "相談内容に対して、タロットカードの意味が否定的なものであれば、その結果をやわらかく、でも明確に伝えてください。\n"
                "ただし、結果をぼかしたりごまかすのではなく、「今はおすすめできません」「課題があります」などの形で伝えてください。\n"
                "その上で、今後の向き合い方や希望が持てる視点を優しく添えてください。\n\n"

                "📌 文体について：\n"
                "- 番号や見出し、記号は使わず、段落ごとに改行して読みやすくしてください。\n"
                "- “一歩踏み込んだ人間らしい語り”を心がけ、占い師らしい視点・経験・思慮を込めて話してください。\n"
                "- 相手が少しでも自分を大切に思えるような言葉を選んでください。\n\n"

                "あなたの言葉は、誰かの心の灯りになります。\n"
                "不安な心にそっと寄り添いながら、カードの意味を通して安心と気づきを届けてください。"
            )

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"相談内容: {question}"}
                ]
            )
            reply = response.choices[0].message.content.strip()

        except Exception as e:
            reply = f"⚠️ エラーが発生しました：{str(e)}"

    return render_template("index.html", reply=reply, card_image_url=card_image_url, selected_card=selected_card, selected_position=selected_position)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

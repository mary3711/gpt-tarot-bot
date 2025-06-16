from flask import Flask, request, render_template
import openai
import os
import random

app = Flask(__name__)

# OpenAI APIキーの取得
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 大アルカナ22枚のカードリスト
cards = [
    "愚者", "魔術師", "女教皇", "女帝", "皇帝", "法王", "恋人", "戦車", "力", "隠者",
    "運命の輪", "正義", "吊るされた男", "死神", "節制", "悪魔", "塔", "星",
    "月", "太陽", "審判", "世界"
]

# 向き：正位置または逆位置
positions = ["正位置", "逆位置"]

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        try:
            question = request.form.get("question")

            # カードと向きをランダムに選ぶ
            selected_card = random.choice(cards)
            selected_position = random.choice(positions)

            # GPTへの指示（systemプロンプト）
            system_prompt = (
                "あなたは、静けさと知性を兼ね備えたプロフェッショナルな女性のタロット占い師です。\n"
                "言葉は丁寧であたたかく、相談者の心に寄り添いながら、安心感と気づきを届けるスタイルを大切にしてください。\n\n"

                "以下のカードと向きがすでに決まっています：\n"
                f"カード：{selected_card} ／ {selected_position}\n\n"

                "🔮 あなたの役割は、上記のカードが表す意味を相談内容にあわせて説明することです。\n\n"

                "💬 回答スタイルのルール：\n"
                "1. 導入では相談内容をきちんと受け止め、やさしく共感してください。\n"
                "2. カードの意味を“相談内容に応じて”噛み砕いて説明してください。\n"
                "3. カードの絵柄や雰囲気の描写は不要です。\n"
                "4. 「〜を教えてくれている」ではなく、「〜を表しています」のような客観的な表現を使ってください。\n"
                "5. 注意点はあくまで“助言としてやわらかく”伝えてください。不安を煽らないでください。\n"
                "6. 「アドバイスとしては〜」などの言い回しは使わず、自然な語りの中で促してください。\n"
                "7. 最後は、相談内容を踏まえた“希望を感じる”言葉で締めくくってください。\n\n"
                "📌 改行を適度に入れて、番号などは使わず読みやすく整えてください。"
            )

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ]

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            reply = response.choices[0].message.content

        except Exception as e:
            reply = f"⚠️ エラーが発生しました：{str(e)}"
            print(f"⚠️ Flaskログ：{str(e)}")

    return render_template("index.html", reply=reply)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=10000)

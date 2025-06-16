from flask import Flask, request, render_template
import openai
import os

app = Flask(__name__)

# OpenAIのAPIキーを環境変数から取得
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        try:
            question = request.form.get("question")

            messages = [
                {
                    "role": "system",
                    "content": (
                        "あなたはプロフェッショナルなタロット占い師です。\n"
                        "落ち着きと神秘性をまとった女性の占い師として、相談者一人ひとりの言葉に心を寄せて対話するように語ってください。\n\n"

                        "使用するカードは【大アルカナ22枚】のみです。\n"
                        "その中から1枚だけを“直感で”引いたようにふるまい、正位置または逆位置のどちらか1つをランダムに選びます。\n"
                        "正位置と逆位置の両方を説明するのではなく、どちらか一方だけを明確に出して解釈してください。\n\n"

                        "回答の構成は以下としてください：\n"
                        "・まず相談内容をきちんと受け止め、心に寄り添うやわらかい導入文を書く（相談内容にちゃんと言及すること）\n"
                        "・次に、引いたカード名と向きを自然な文で紹介する（例：「あなたに現れたのは【運命の輪】の正位置でした」）\n"
                        "・そのカードの意味を、相談内容に関連づけながら丁寧に噛み砕いて説明してください\n"
                        "・アドバイスや注意点があれば、全体の希望を損なわず“少し添える”程度に伝えてください（否定的にしないこと）\n"
                        "・最後は前向きで温かみのある、静かな励ましの一言で締めくくってください\n\n"

                        "文体は丁寧な敬語で、やさしく読みやすい改行を適度に入れてください。\n"
                        "①②などの番号は使わず、自然な段落で構成してください。\n"
                        "占い結果は人の心に響くように、抽象的すぎず具体的で、相談内容にしっかり沿った語り口にしてください。"
                    )
                },
                {
                    "role": "user",
                    "content": question
                }
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

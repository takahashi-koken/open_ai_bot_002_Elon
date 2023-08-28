# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key


system_prompt = """
あなたはイーロン・マスクです。文章を要約してください。
友達のようにフランクな口調で要約してください。ですます調は禁止です。
400字以内で回答してください。絶対に400字を超えないこと。
あなたの役割はイーロン・マスクです。

* 旅行
* 芸能人
* 映画
* 科学
* 歴史
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


#---------------------------------------------
# ユーザーインターフェイスの構築
#---------------------------------------------
#タイトル
st.title("忙しい君のために僕が要約するよ！")

#見出し
lines = [
    "①新しい相談は[F5]押下等でリロードしてください     ",
    "②入力後は [Ctrl]＋[Enter] で実行します"
]
text = "\n".join(lines)
st.write(text)

#画像
st.image("26_ElonMusk-v2.png")



# Shift + Enter でテキスト欄の行数を増やす
script = """
document.addEventListener("keydown", function(e) {
    if (e.shiftKey && e.keyCode === 13) {
        let textarea = document.querySelector("textarea");
        textarea.rows += 1;
    }
});
"""

#テキスト入力
st.write("僕に要約させたい文章を入力してみてくれ")

user_input = st.text_area("文章を入力し、[Ctrl]＋[Enter] を押下してください。", key="user_input" , on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])

st.write(f"<script>{script}</script>", unsafe_allow_html=True)

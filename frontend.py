import streamlit as st
import requests

st.set_page_config(
    page_title="SHL Chatbot"
)

st.title(
    "🤖 SHL Assessment Recommendation Bot"
)

st.write(
    "Ask hiring requirements and get SHL assessment recommendations."
)

user_input = st.text_input(
    "Enter hiring requirements"
)

if st.button("Send"):

    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ]
    }

    response = requests.post(
        "https://shl-agent-production-beee.up.railway.app/chat",
        json=payload
    )

    data = response.json()

    st.subheader("Bot Reply")
    st.write(data["reply"])

    if data["recommendations"]:

        st.subheader("Recommendations")

        for rec in data["recommendations"]:

            st.write(
                f"✅ {rec['name']} ({rec['test_type']})"
            )

            st.write(rec["url"])
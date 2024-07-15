from financialgpt.core import FinancialGPT
import streamlit as st

st.set_page_config(
    page_title="FinancialGPT",  # This is the new page title
    page_icon="🪙",  # This is the new page icon. You can use emoji or a URL to an image.
)

st.title("FinancialGPT - Motive Partners")

model = FinancialGPT()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_text = model.invoke(prompt)
        st.markdown(response_text)
        st.session_state.messages.append(
            {"role": "assistant", "content": response_text}
        )

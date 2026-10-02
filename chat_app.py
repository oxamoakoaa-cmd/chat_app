import os

import streamlit as st
from openai import OpenAI


MODEL = "meta-llama/Llama-3.1-8B-Instruct:novita"
BASE_URL = "https://router.huggingface.co/v1"

st.set_page_config(page_title="AI Chat", page_icon="💬", layout="centered")

with st.sidebar:
    st.title("AI Chat")
    st.caption("Hugging Face model")
    if st.button("New chat", icon="🗑️", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Chat")
st.caption("Ask a question to start a conversation.")

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("Hi! What would you like to talk about?")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message the assistant..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        token = "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"
        if not token:
            st.error("Set the HF_TOKEN environment variable to connect to Hugging Face.")
        else:
            try:
                client = OpenAI(base_url=BASE_URL, api_key=token)
                with st.spinner("Thinking..."):
                    completion = client.chat.completions.create(
                        model=MODEL,
                        messages=st.session_state.messages,
                    )
                answer = completion.choices[0].message.content or "I couldn't generate a response."
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as error:
                st.error(f"Unable to get a response: {error}")
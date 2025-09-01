import os
import streamlit as st
import google.generativeai as genai

# Konfigurasi API pakai ENV variable
genai.configure(api_key="AIzaSyANKcW1bcGKcHBaaBlUPdUFKiTKER9acb0")

# Load model
model = genai.GenerativeModel("gemini-1.5-flash")

st.set_page_config(page_title="Eko Chatbot", page_icon="🤖")
st.title("🤖 Eko Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input user
if prompt := st.chat_input("Tulis pesan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = model.generate_content(prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            message_placeholder.error(f"Error: {e}")

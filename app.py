import streamlit as st
import google.generativeai as genai

# Konfigurasi API (langsung hardcode atau pakai ENV)
genai.configure(api_key="AIzaSyANKcW1bcGKcHBaaBlUPdUFKiTKER9acb0")

# Pakai model Gemini
model = genai.GenerativeModel("gemini-2.5-flash")

st.set_page_config(page_title="Eko Chatbot", page_icon="🤖")
st.title("🤖 Eko Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan history
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
        full_response = ""

        try:
            # Mode streaming
            for chunk in model.generate_content(prompt, stream=True):
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")  # efek cursor
            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            message_placeholder.error(f"Error: {e}")

import time
import streamlit as st
from utils import load_chain

compnay_logo = 'https://www.app.nl/wp-content/uploads/2019/01/Blendle.png'

st.set_page_config(
    page_title = "Gyehwan Notion Chatbot",
    page_icon = compnay_logo
)

chain = load_chain

if 'message' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant",
                                     "content": "Hi human! How can I help you today?"}]

for message in st.session_state.messages:
    if message["role"] == 'assistant':
        with st.chat_message(["role"], avatart=compnay_logo):
            st.markdown(message["content"])
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
if query := st.chain_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
        
    with st.chat_message("assistant", avatar=compnay_logo):
        message_placeholder = st.empty()
        result = chain({"question": query})
        response = result['answer']
        full_response = ""
        
        for chunk in response.split():
            full_response += chunk + ""
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": response})
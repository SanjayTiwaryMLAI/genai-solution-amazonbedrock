# importing required modules 
from basefunction import claudemodel
import streamlit as st
import io
#st. set_page_config(layout="wide") 
import streamlit as st

#add sidebar and connect a page
st.sidebar.title("Chatbot")
st.sidebar.caption("A streamlit chatbot powered by LLM", )
st.sidebar.markdown("##")
#connect to another sheet


st.sidebar.title("Document analysis")
st.sidebar.caption("A Bedrock powered LLM")
st.sidebar.code('Write a blog post on deploying LLAMA2 model on AWS inferentia chip')
#st.sidebar.


st.title("💬 Chatbot")
st.caption("🚀 A streamlit chatbot powered by LLM")

#create 2 colomn
col1, col2 = st.columns(2)

#define col1
with col1:
    max_token = st.number_input("Enter the max token", min_value=1, max_value=2000, value=500, step=10)
    st.write('Current value of max_tokens_to_sample is', max_token)
# create a button to enter value for max token in integer
with col2:
    temperature = st.number_input("Enter the temperature" ,min_value=0.0, max_value=1.0, step= 0.1)
    st.write('Current value of temperature is', temperature)


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = claudemodel(prompt, max_token, temperature)
    msg = response
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


#clear session state button
clear_button = st.button("Clear session state")
if clear_button:
    st.session_state.clear()
    st.experimental_rerun()

# importing required modules 
from claude3basefunction import Analyticsfunction
from basefunction import count_tokens

import base64
import streamlit as st
st. set_page_config(layout="wide") 
import io
# create logo using image on Streamlit app
st.set_option('deprecation.showPyplotGlobalUse', False)
st.markdown("# 💡 Math question and answer using Claude3")
st.sidebar.header("🤖 Document Analysis")

st.sidebar.caption("streamlit chatbot powered by LLM")

# create a dropdown in sidebar for selection of model from streamlit sidebar


st.write(
    """The ability for Claude 3 to process images is a game-changer. Think about automating tasks that involve user-uploaded content or quickly analyzing charts and graphs without manual input. Claude 3 can handle:
Photos
Charts and graphs
Technical diagrams
This opens up a ton of possibilities for creating more interactive and intelligent applications, like auto captioning.
"""
)

obj = Analyticsfunction()

convert_image =  obj.convert_image_to_base64
claude3 = obj.call_claude_sonet

def invoke_model( question, image):
    base64_image = convert_image(image)
    response = claude3(base64_image,question)
    num_tokens = count_tokens(response)
    
    st.info(f"Output contains {num_tokens} tokens.")
    #st.write(f"Output contains {num_tokens} tokens.")
    
    st.write(response)
    st.download_button(data=response, label="download")
          
    with open("response.txt", "w") as f:
        f.write(response)
        f.close()


#Display image
def display_image(image_path):
    with open(image_path, "rb") as f:
        image_data = f.read()
    st.image(image_data, use_column_width=True)


image = st.file_uploader("UPLOAD A IMAGE")
if image:
    st.write("Image uploaded successfully")
    output = open("file01.jpg", "wb")
    output.write(image.read())
    output.close()
    #response = image_to_text("file01.jpg")
    #wait for response is recieved\
    #st.write(response)
    display_image("file01.jpg")

enterinput = st.text_input("Ask any question from document" )
ask_button1 = st.button("Re-Enter")
if ask_button1:
    invoke_model(enterinput,"file01.jpg")


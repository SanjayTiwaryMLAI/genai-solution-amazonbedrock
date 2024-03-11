# importing required modules 
from basefunction import pdfuplaodllmmodel as pdfu
from basefunction import pdfuplaodllmmodelselection as pdfus
from basefunction import translate_to_hindi
from basefunction import detect_sentiment
from basefunction import mask_pii
from basefunction import count_tokens
from basefunction import detect_entity
from basefunction import send_response_to_s3
from basefunction import text_to_speech
from printcloud import print_wordcloud
import base64
import numpy as np
import streamlit as st
st. set_page_config(layout="wide") 
st.set_option('deprecation.showPyplotGlobalUse', False)
import io
# create logo using image on Streamlit app

st.markdown("# 💡 Multipage PDF analysis using Bedrock")
st.sidebar.header("🤖 Document Analysis")
st.sidebar.text("1. Amazon Bedrock - LLM" )
st.sidebar.text("2. Amazon Traslate -translation")
st.sidebar.text("3. Amazon Comprehend- entities detection")
st.sidebar.text("4. Amazon Polly -Text to Speech")
st.sidebar.caption("streamlit chatbot powered by LLM")

# create a dropdown in sidebar for selection of model from streamlit sidebar

add_selectbox = st.sidebar.selectbox(
    "Select the Bedrock LLM",
    ("anthropic.claude-v2:1", "anthropic.claude-v2", "anthropic.claude-v1")
)

st.write(f"Model selected is: :blue[{add_selectbox}]")


st.write(
    """This demo illustrates the power of Large Language model for analysis of PDF file, 
    here the LLM is used for creating summary and generating questiom answers and many more, Enjoy!"""
)

#st.title(":blue[Document analysis using Large Language Model ]", )
uploaded_file = st.file_uploader("Choose a file")


def invoke_model(modelid, question, file, maxtoken, temperature):
    response = pdfus(modelid, question,file, maxtoken, temperature)
    num_tokens = count_tokens(response)
    
    st.info(f"Output contains {num_tokens} tokens.")
    #st.write(f"Output contains {num_tokens} tokens.")
    
    st.write(response)
    st.download_button(data=response, label="download")
          
    with open("response.txt", "w") as f:
        f.write(response)
        f.close()

#create 2 colomn
col1, col2 = st.columns(2)

#define col1
with col1:
    max_token = st.number_input("Enter the max token", min_value=1, max_value=20000, value=500, step=10)
    st.write('Current value of max_tokens_to_sample is', max_token)
# create a button to enter value for max token in integer
with col2:
    temperature = st.number_input("Enter the temperature" ,min_value=0.0, max_value=1.0, step= 0.1)
    st.write('Current value of temperature is', temperature)

def displayPDF(file):
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Embedding PDF in HTML
    pdf_display = F'<embed src="data:application/pdf;base64,{base64_pdf}" width="1000" height="500" type="application/pdf">'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True, )

# check if the file is uploaded
if uploaded_file is not None:
    # read the file
    pdf_data = uploaded_file.read()
    # create a pdf file object
    pdf_file = io.BytesIO(pdf_data)

    # save the pdf file to a file
    with open("pdf_file.pdf", "wb") as f:
        f.write(pdf_data)
        f.close()
        st.write("File saved to pdf_file.pdf")
        #create function to display the uploaded pdf file in UI
        displayPDF("pdf_file.pdf")           

def create_dropdown(options):
    dropdown = st.selectbox("Select a question type:", options)
    return dropdown


options = ["Please write a summary of document in 200 words","Please write a summary of document in 200 words in hindi", "please write top 5 insights of the document", "create 5 point summary in 100 words", "Please write 10 FAQ based on document" ,"create 5 questions and answer "]
selected = create_dropdown(options)
ask_button = st.button("Ask to model based on question selected")
    # check if the button is clicked
if ask_button:
    invoke_model(add_selectbox, selected,uploaded_file, max_token, temperature)


enterinput = st.text_input("Ask any question from document" )
ask_button1 = st.button("Ask to model based input")
if ask_button1:
    invoke_model(add_selectbox,enterinput,uploaded_file, max_token, temperature) 
    #
    #detect PII

st.header("Enhancements using Amazon AI services")
tab1,tab2,tab3,tab4,tab5,tab6,tab7 = st.tabs(["TRANSLATE --> HINDI", "SEND--> S3", "DETECT SENTIMENT","SHOW ENTITIES", "DETECT PII", "PRINT WORDCLOUD", "CONVERT INTO SPEECH"])

with tab1:
    ask_button = st.button("Get Translation")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        translated_response = translate_to_hindi(response)
                # display the translated response
        st.write(translated_response)

with tab2:
   ask_button = st.button("Send to S3")
   if ask_button:
        with open("response.txt", "r") as f:

                response = f.read()
                f.close()

        local_file_path = response  # Path to your local file
        bucket_name = 'opensearchdemosanjay'  # Name of your S3 bucket
        s3_file_name = 'response.txt'
        region= "us-east-1"  # Name you want to give the file in the S3 bucket

        path= send_response_to_s3(local_file_path, bucket_name, s3_file_name, region)
        st.success("Response sent to S3")
        st.write("file is coped to-", path)

with tab3:
    ask_button = st.button("Get Sentiment")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        sentiment = detect_sentiment(response)
        st.write(sentiment)

with tab4:
    ask_button = st.button("Get Entities")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        detectentity = detect_entity(response)
        for i in range(0, len(detectentity)):
            type = (detectentity[i]["Type"])
            Text = (detectentity[i]["Text"])
            st.write(type, "-->" , Text)

with tab5:
    ask_button = st.button("Get PII")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        masked_response = mask_pii(response)
        for i in range(0, len(masked_response)):
            type = (masked_response[i]["Type"])
            score = (masked_response[i]["Score"])
            st.write(type, "-->", score)

with tab6:
    ask_button = st.button("Get Wordcloud")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        print_wordcloud(response)
        st.pyplot()

with tab7:
    ask_button = st.button("Get Speech")
    if ask_button:
        with open("response.txt", "r") as f:
            response = f.read()
            f.close()
        #st.write(response)
        text_to_speech(response)

        audio_file = open('speech.mp3', 'rb')
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format='audio/ogg')   



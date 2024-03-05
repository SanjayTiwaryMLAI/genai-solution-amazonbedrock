import streamlit as st
import uuid
import sys
from basefunction import send_response_to_s3

import kendra_retriever_samples.kendra_chat_bedrock_claudev2 as bedrock_claudev2

#st.set_page_config(layout="centered" ) 

st.title("🔎 GEN AI based search using RAG" )

st.sidebar.title("RAG developed using Amazon Kendra and Bedrock")
st.sidebar.caption("LLM- Anthropic Claude2")
st.sidebar.text("Which are the APIs for milestone 1/2/3")
st.sidebar.text("How does a user can search his/her medical records and explain step by step?")

#st.sidebar.

import boto3
import time
s3 = boto3.client('s3', region_name="ap-south-1")

def sync_kendra_index(Id, IndexId):
    session = boto3.session.Session(region_name="ap-south-1")
    kendra_client = session.client('kendra')
    
    try:
        response = kendra_client.start_data_source_sync_job(Id= Id,IndexId= IndexId)
        print(response)
        #wait for the sync job to complete
        while True: 
            with st.spinner('Wait for it...'):
                    time.sleep(5)         
            response = kendra_client.list_data_source_sync_jobs(Id= Id, IndexId= IndexId)
            if response['History'][0]['Status'] == 'SUCCEEDED':
                st.write("Data source sync job succeeded.")
                break
            elif response['History'][0]['Status'] == 'FAILED':
                st.write("Data source sync job failed.")
                break           
    
    except kendra_client.exceptions.ValidationException as e:
        print(f"Error syncing index: {e}")
        
    print(f"Sync triggered for {len(Id)} data sources")

def display_file_from_s3(bucket):
    s3 = boto3.client('s3', region_name="ap-south-1")
    file_object = s3.list_objects(Bucket=bucket)
    for i in range(0,len(file_object["Contents"])):
        st.write(file_object["Contents"][i]["Key"])   



#create a button to start sync of Amazon Kendra
index_id = "2c5ae64e-a382-4ae9-bb90-deb069c662fa" 
id = "e385cde4-178f-4e3a-bf7d-61b58b41fd3c"

st.sidebar.markdown("## Sync Amazon Kendra")
if st.sidebar.button("Sync Amazon Kendra"):
    sync_kendra_index(id, index_id)
    st.success("Syncing Amazon Kendra")


USER_ICON = "kendra_retriever_samples/images/user-icon.png"
AI_ICON = "kendra_retriever_samples/images/ai-icon.png"
MAX_HISTORY_LENGTH = 5
PROVIDER_MAP = {
    'anthropic': 'Anthropic',
    'llama2' : 'Llama 2'
}

#function to read a properties file and create environment variables
def read_properties_file(filename):
    import os
    import re
    with open(filename, 'r') as f:
        for line in f:
            m = re.match(r'^\s*(\w+)\s*=\s*(.*)\s*$', line)
            if m:
                os.environ[m.group(1)] = m.group(2)


# Check if the user ID is already stored in the session state
if 'user_id' in st.session_state:
    user_id = st.session_state['user_id']

# If the user ID is not yet stored in the session state, generate a random UUID
else:
    user_id = str(uuid.uuid4())
    st.session_state['user_id'] = user_id


if 'llm_chain' not in st.session_state:
    st.session_state['llm_app'] = bedrock_claudev2
    st.session_state['llm_chain'] = bedrock_claudev2.build_chain()

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
if "chats" not in st.session_state:
    st.session_state.chats = [
        {
            'id': 0,
            'question': '',
            'answer': ''
        }
    ]

if "questions" not in st.session_state:
    st.session_state.questions = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "input" not in st.session_state:
    st.session_state.input = ""


st.markdown("""
        <style>
               .block-container {
                    padding-top: 32px;
                    padding-bottom: 32px;
                    padding-left: 0;
                    padding-right: 0;
                }
                .element-container img {
                    background-color: #000000;
                }

                .main-header {
                    font-size: 24px;
                }
        </style>
        """, unsafe_allow_html=True)

def write_logo():
    col1, col2, col3 = st.columns([5, 1, 5])
    with col2:
        st.image(AI_ICON, use_column_width='always') 


def write_top_bar():
    col1, col2, col3 = st.columns([1,10,2])
    with col1:
        st.image(AI_ICON, use_column_width='always')
    with col2:
        selected_provider = "bedrock_claudev2"
        if selected_provider in PROVIDER_MAP:
            provider = PROVIDER_MAP[selected_provider]
        else:
            provider = selected_provider.capitalize()
        header = f"Ask any question?"
        st.write(f"<h3 class='main-header'>{header}</h3>", unsafe_allow_html=True)
    with col3:
        clear = st.button("Clear Chat")
    return clear

clear = write_top_bar()

if clear:
    st.session_state.questions = []
    st.session_state.answers = []
    st.session_state.input = ""
    st.session_state["chat_history"] = []

def handle_input():
    input = st.session_state.input
    question_with_id = {
        'question': input,
        'id': len(st.session_state.questions)
    }
    st.session_state.questions.append(question_with_id)

    chat_history = st.session_state["chat_history"]
    if len(chat_history) == MAX_HISTORY_LENGTH:
        chat_history = chat_history[:-1]

    llm_chain = st.session_state['llm_chain']
    chain = st.session_state['llm_app']
    result = chain.run_chain(llm_chain, input, chat_history)
    answer = result['answer']
    chat_history.append((input, answer))
    
    document_list = []
    if 'source_documents' in result:
        for d in result['source_documents']:
            if not (d.metadata['source'] in document_list):
                document_list.append((d.metadata['source']))

    st.session_state.answers.append({
        'answer': result,
        'sources': document_list,
        'id': len(st.session_state.questions)
    })
    st.session_state.input = ""

def write_user_message(md):
    col1, col2 = st.columns([1,12])
    
    with col1:
        st.image(USER_ICON, use_column_width='always')
    with col2:
        st.warning(md['question'])


def render_result(result):
    answer, sources = st.tabs(['Answer', 'Sources'])
    with answer:
        render_answer(result['answer'])
    with sources:
        if 'source_documents' in result:
            render_sources(result['source_documents'])
        else:
            render_sources([])

def render_answer(answer):
    col1, col2 = st.columns([1,12])
    with col1:
        st.image(AI_ICON, use_column_width='always')
    with col2:
        st.info(answer['answer'])

def render_sources(sources):
    col1, col2 = st.columns([1,12])
    with col2:
        with st.expander("Sources"):
            for s in sources:
                st.write(s)

    
#Each answer will have context of the question asked in order to associate the provided feedback with the respective question
def write_chat_message(md, q):
    chat = st.container()
    with chat:
        render_answer(md['answer'])
        render_sources(md['sources'])
    
        
with st.container():
  for (q, a) in zip(st.session_state.questions, st.session_state.answers):
    write_user_message(q)
    write_chat_message(a, q)

st.markdown('---')
input = st.text_input("You are talking to an AI, ask any question.", key="input", on_change=handle_input)
import io
#create upload button from streamlit ui for uploading file to S3
st.sidebar.markdown("## Upload File")
file = st.sidebar.file_uploader("Upload file", type=["pdf", "docx", "txt"])
if file is not None:
    # read the file
    pdf_data = file.read()
    # create a pdf file object
    pdf_file = io.BytesIO(pdf_data)

    # save the pdf file to a file
    with open("pdf_file.pdf", "wb") as f:
        f.write(pdf_data)
        f.close()
        st.write("File saved to pdf_file.pdf")
        #create function to display the uploaded pdf file in UI

#send file to amazon S3
if file is not None:
    local_file_path = 'pdf_file.pdf'  # Path to your local file
    bucket_name = 'document-tendermum'  # Name of your S3 bucket
    s3_file_name = 'pdf_file.pdf' 
    region = "ap-south-1" # Name you want to give the file in the S3 bucket

    path= send_response_to_s3(local_file_path, bucket_name, s3_file_name,region)

    st.write("file is coped to-", path)
    #s3.upload_file(file, 'opensearchdemosanjay', 'file.pdf')
    st.success("File copied to S3")
    display_file_from_s3("document-tendermum")  
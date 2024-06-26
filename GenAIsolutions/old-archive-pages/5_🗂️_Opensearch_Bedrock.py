import streamlit as st

import components.authenticate as authenticate
st.set_page_config(layout="wide" )

# Check authentication
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()


if (
    st.session_state["authenticated"]
    and "adminaccess" in st.session_state["user_cognito_groups"]
):
    st.set_option('deprecation.showPyplotGlobalUse', False)
    import io
    # create logo using image on Streamlit app
    
    import coloredlogs
    import logging
    import argparse
    from opensearch.utils import opensearch, secret
    from langchain.embeddings import BedrockEmbeddings
    from langchain.vectorstores import OpenSearchVectorSearch
    from langchain.chains import RetrievalQA
    from langchain.prompts import PromptTemplate
    from langchain.llms.bedrock import Bedrock
    import boto3
    
    
    st.title("🔎  RAG implemented using Opensearch and Bedrock" )
    st.sidebar.title("RAG developed using Opensearch and Bedrock")
    st.sidebar.caption("LLMs- Anthropic Claude2")
    st.sidebar.text("How is Amazon performed during Covid19")
    st.sidebar.text("What are various challenges Amazon faced")
    
    coloredlogs.install(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%H:%M:%S', level='INFO')
    logging.basicConfig(level=logging.INFO) 
    logger = logging.getLogger(__name__)
    
    def parse_args():
        parser = argparse.ArgumentParser()
        parser.add_argument("--ask", type=str, default="What is <3?")
        parser.add_argument("--index", type=str, default="rag")
        parser.add_argument("--region", type=str, default="us-east-1")
        parser.add_argument("--bedrock-model-id", type=str, default="anthropic.claude-v2")
        parser.add_argument("--bedrock-embedding-model-id", type=str, default="amazon.titan-embed-text-v1")
        
        return parser.parse_known_args()
    
    
    def get_bedrock_client(region):
        bedrock_client = boto3.client("bedrock-runtime", region_name=region)
        return bedrock_client
        
    
    def create_langchain_vector_embedding_using_bedrock(bedrock_client, bedrock_embedding_model_id):
        bedrock_embeddings_client = BedrockEmbeddings(
            client=bedrock_client,
            model_id=bedrock_embedding_model_id)
        return bedrock_embeddings_client
        
    
    def create_opensearch_vector_search_client(index_name, opensearch_password, bedrock_embeddings_client, opensearch_endpoint, _is_aoss=False):
        docsearch = OpenSearchVectorSearch(
            index_name=index_name,
            embedding_function=bedrock_embeddings_client,
            opensearch_url=f"https://{opensearch_endpoint}",
            http_auth=(index_name, opensearch_password),
            is_aoss=_is_aoss
        )
        return docsearch
    
    
    def create_bedrock_llm(bedrock_client, model_version_id):
        bedrock_llm = Bedrock(
            model_id=model_version_id, 
            client=bedrock_client,
            model_kwargs={"max_tokens_to_sample": 100,'temperature': 0}
            )
        return bedrock_llm
        
    
    def main():
        logging.info("Starting")
        args, _ = parse_args()
        region = args.region
        index_name = args.index
        bedrock_model_id = args.bedrock_model_id
        bedrock_embedding_model_id = args.bedrock_embedding_model_id
        
        # Creating all clients for chain
        bedrock_client = get_bedrock_client(region)
        bedrock_llm = create_bedrock_llm(bedrock_client, bedrock_model_id)
        bedrock_embeddings_client = create_langchain_vector_embedding_using_bedrock(bedrock_client, bedrock_embedding_model_id)
        opensearch_endpoint = opensearch.get_opensearch_endpoint(index_name, region)
        opensearch_password = secret.get_secret(index_name, region)
        opensearch_vector_search_client = create_opensearch_vector_search_client(index_name, opensearch_password, bedrock_embeddings_client, opensearch_endpoint)
        
        #ask question from streamlit ui
        #st.title("Ask a question")
        question = st.text_input("Enter your question here:")
        # if st.button("Submit"):
        #     question = question1
    
        # # LangChain prompt template
        # if len(args.ask) > 0:
        #     question = question
       
        
        prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. don't include harmful content
    
        {context}
    
        Question: {question}
        Answer:"""
        PROMPT = PromptTemplate(
            template=prompt_template, input_variables=["context", "question"]
        )
        
        logging.info(f"Starting the chain with KNN similarity using OpenSearch, Bedrock FM {bedrock_model_id}, and Bedrock embeddings with {bedrock_embedding_model_id}")
        
        qa = RetrievalQA.from_chain_type(llm=bedrock_llm, 
                                         chain_type="stuff", 
                                         retriever=opensearch_vector_search_client.as_retriever(),
                                         return_source_documents=True,
                                         chain_type_kwargs={"prompt": PROMPT, "verbose": False},
                                         verbose=False)
        
        if st.button("Submit"):
            logging.info(f"The question is: {question}")
            st.text(f"The question is: {question}")
            response = qa(question, return_only_outputs=False)
    
            logging.info("This are the similar documents from OpenSearch based on the provided query")
            source_documents = response.get('source_documents')
            for d in source_documents:
                logging.info(f"With the following similar content from OpenSearch:\n{d.page_content}\n")
                #logging.info(f"Text: {d.metadata['text']}")
                #st.write(f"With the following similar content from OpenSearch:\n{d.page_content}\n")
                #st.write(f"Text: {d.metadata['text']}")
            
            logging.info(f"The answer from Bedrock {bedrock_model_id} is: {response.get('result')}")
            st.text(f"The answer from Bedrock {bedrock_model_id}")
            st.write(response.get('result'))
        
    
    if __name__ == "__main__":
        main()
        



else:
    if st.session_state["authenticated"]:
        st.write("You do not have access. Please contact the administrator.")
    else:
        st.write("Please login!")


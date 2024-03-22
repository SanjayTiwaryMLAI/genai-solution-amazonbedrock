import streamlit as st



st.set_page_config(
    page_title="Hello",
    page_icon="👋",layout="wide"
)

st.write("# 🚀 Welcome to Generative AI Demo using Amazon Bedrock! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    1. Amazon Bedrock is a fully managed service that offers a choice of high-performing foundation models (FMs) from leading AI companies like AI21 Labs, Anthropic, Cohere, Meta, Stability AI, and Amazon via a single API, along with a broad set of capabilities you need to build generative AI applications with security, privacy, and responsible AI. 
    2. Using Amazon Bedrock, you can easily experiment with and evaluate top FMs for your use case, privately customize them with your data using techniques such as fine-tuning and Retrieval Augmented Generation (RAG), and build agents that execute tasks using your enterprise systems and data sources. 
    3. Since Amazon Bedrock is serverless, you don't have to manage any infrastructure, and you can securely integrate and deploy generative AI capabilities into your applications using the AWS services you are already familiar with.
    
    **👈 Select a demo from the sidebar** to see some examples
   
    ### Want to learn more?
    - Check out [Amazon Bedrock](https://aws.amazon.com/bedrock/)
    - Jump into our [FAQ](https://aws.amazon.com/bedrock/faqs/)
    - Check out our [Blog](https://aws.amazon.com/blogs/machine-learning/category/artificial-intelligence/amazon-machine-learning/amazon-bedrock/)
"""
)
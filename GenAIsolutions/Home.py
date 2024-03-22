import streamlit as st
import components.authenticate as authenticate

st.set_page_config(
    page_title="Hello",
    page_icon="👋",layout="wide"
)
st.write("# Welcome to Streamlit! 👋")

st.markdown(
    """
    Streamlit is an open-source app framework built specifically for
    Machine Learning and Data Science projects.
    **👈 Select a demo from the sidebar** to see some examples
    of what Streamlit can do!
    ### Want to learn more?
    - Check out [streamlit.io](https://streamlit.io)
    - Jump into our [documentation](https://docs.streamlit.io)
    - Ask a question in our [community
        forums](https://discuss.streamlit.io)
    ### See more complex demos
    - Use a neural net to [analyze the Udacity Self-driving Car Image
        Dataset](https://github.com/streamlit/demo-self-driving)
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# Check authentication when user lands on the home page.
authenticate.set_st_state_vars()

# Add login/logout buttons
if st.session_state["authenticated"]:
    authenticate.button_logout()
else:
    authenticate.button_login()

# if st.session_state["authenticated"] and "Underwriters" in st.session_state["user_cognito_groups"]:
#     st.write(
#         """This demo illustrates a combination of plotting and animation with
#     Streamlit. We're generating a bunch of random numbers in a loop for around
#     5 seconds. Enjoy!"""
#     )

#     # ...
# else:
#     if st.session_state["authenticated"]:
#         st.write("You do not have access. Please contact the administrator.")
#     else:
#         st.write("Please login!")
    
    import streamlit as st


st.write("# 🚀 Welcome to Generative AI Demo using Amazon Bedrock! 👋")

st.sidebar.success("Select a demo above.")

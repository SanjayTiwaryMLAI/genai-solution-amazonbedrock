
import boto3
from streamlit_aws_auth import Auth, CognitoUserPoolAuthorizer

# Initialize Cognito authentication
cog_auth = CognitoUserPoolAuthorizer(
    user_pool_id="my_user_pool_id", 
    user_pool_client_id="6avbau3bonk5478jml3hft5t9a",
    region="us-east-1"
)

# Create the Auth object
auth = Auth(
    authorizers=[cog_auth], 
    on_failure_redirect_to_authorization_url=True,
    authorization_url=cog_auth.authorization_url
)

# Secure the entire app with Auth 
def main():

    auth.login_button()

    # User authenticated, run app
    authenticated_user = auth.get_user()
    
    # Rest of Streamlit app
    import streamlit as st

    st.title("Sign Up")

    username = st.text_input("Username")
    password = st.text_input("Password", type='password')

    if st.button("Sign Up"):
        client = get_cognito_client()
        sign_up(client, username, password)
        st.success("User created! Please check your email for a confirmation code.")
  

    # When the user signs up, call the `sign_up` function to create the user in Cognito. This will trigger a confirmation email.

    # 2. Create a confirmation page:

    # ```python
    st.title("Confirm Sign Up") 

    username = st.text_input("Username")
    code = st.text_input("Confirmation Code")

    if st.button("Confirm"):
        client = get_cognito_client()
        confirm_sign_up(client, username, code)
        st.success("Confirmed!")
    # ```

    # The user enters their confirmation code from the email to confirm their account.

    # 3. Add routes or logic to switch between pages:

    # ```python 
    page = st.sidebar.selectbox("Choose page", ["Sign Up", "Confirm"])
    
    if page == "Sign Up":
        st.write("Sign Up")
    
    elif page == "Confirm":
        st.write("Confirm")
if __name__ == "__main__":
    main()

# Helper functions for Cognito integration
def get_cognito_client():
    client = boto3.client(
        "cognito-idp", 
        region_name="us-east-1"
    )
    return client

def sign_up(client, username, password):
    try:
        resp = client.sign_up(
            ClientId='my_app_client_id',
            Username=username,
            Password=password
        )
        print(resp)
    except Exception as e:
        print(e)
        
def confirm_sign_up(client, username, code):
    try:
        resp = client.confirm_sign_up(
            ClientId='my_app_client_id',
            Username=username, 
            ConfirmationCode=code
        )
        print(resp)
    except Exception as e:
        print(e)  

